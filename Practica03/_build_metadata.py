import re, json, pathlib, collections, datetime
src=pathlib.Path('backups/240485_27.10.26.sql').read_text(encoding='utf-8',errors='replace')
tables={}
for m in re.finditer(r'CREATE TABLE\s+`([^`]+)`\s*\((.*?)\)\s*ENGINE\s*=\s*([^;]+);',src,re.I|re.S):
    name,body,engine=m.group(1),m.group(2),m.group(3)
    t={'name':name,'engine':engine.split()[0],'columns':[],'indexes':[],'checks':[],'primaryKey':[],'foreignKeys':[],'rows':None,'countStatus':'Conteo no disponible en el respaldo','entityType':'Fuerte'}
    for raw in body.splitlines():
        line=raw.strip().rstrip(',')
        cm=re.match(r'`([^`]+)`\s+(.+)',line)
        if cm:
            col,rest=cm.groups()
            typem=re.match(r'([a-zA-Z]+(?:\s+unsigned)?(?:\s+zerofill)?)\s*(\([^)]*\))?',rest,re.I)
            typ=typem.group(1).upper() if typem else rest.split()[0].upper()
            size=typem.group(2)[1:-1] if typem and typem.group(2) else None
            enumvals=re.findall(r"'((?:\\'|[^'])*)'",size or '') if typ in ('ENUM','SET') else []
            null='NOT NULL' not in rest.upper()
            defaultm=re.search(r'\bDEFAULT\s+((?:\'[^\']*\')|(?:b\'[^\']*\')|(?:CURRENT_TIMESTAMP(?:\(\))?)|(?:NULL)|(?:[^\s,]+))',rest,re.I)
            coldata={'name':col,'type':typ+(f'({size})' if size else ''),'length':None,'precision':None,'scale':None,'nullable':null,'default':defaultm.group(1) if defaultm else None,'autoIncrement':'AUTO_INCREMENT' in rest.upper(),'primaryKey':False,'foreignKeys':[],'unique':False,'checks':[],'indexes':[],'enumValues':enumvals,'technicalDomain':typ+(f'({size})' if size else ''),'functionalDomain':'Dominio funcional no especificado en el respaldo','classification':{'values':'Monovalorado (inferido)','composition':'Simple (inferido)','storage':'Almacenado','required':'Opcional' if null else 'Obligatorio','function':'Atributo no clave','nature':'Temporal' if any(x in typ for x in ['DATE','TIME','YEAR']) else ('Cuantitativa' if any(x in typ for x in ['INT','DECIMAL','FLOAT','DOUBLE','BIT']) else 'Cualitativa nominal'),'confidence':'Inferida; validar según reglas de negocio'}}
            if size and typ not in ('ENUM','SET'):
                nums=[int(x) for x in size.split(',') if x.strip().isdigit()]
                if len(nums)==1: coldata['length']=nums[0]
                elif len(nums)==2: coldata['precision'],coldata['scale']=nums
            t['columns'].append(coldata); continue
        pm=re.match(r'PRIMARY KEY\s*\((.*?)\)',line,re.I)
        if pm:
            t['primaryKey']=re.findall(r'`([^`]+)`',pm.group(1)); continue
        fm=re.match(r'(?:CONSTRAINT\s+`([^`]+)`\s+)?FOREIGN KEY\s*\((.*?)\)\s+REFERENCES\s+`([^`]+)`\s*\((.*?)\)(.*)',line,re.I)
        if fm:
            cols=re.findall(r'`([^`]+)`',fm.group(2)); refcols=re.findall(r'`([^`]+)`',fm.group(4)); namekey=fm.group(1) or f'FK_{name}_{len(t["foreignKeys"])+1}'; tail=fm.group(5)
            t['foreignKeys'].append({'name':namekey,'columns':cols,'targetTable':fm.group(3),'targetColumns':refcols,'onDelete':(re.search(r'ON DELETE (CASCADE|SET NULL|RESTRICT|NO ACTION)',tail,re.I) or [None,None])[1],'onUpdate':(re.search(r'ON UPDATE (CASCADE|SET NULL|RESTRICT|NO ACTION)',tail,re.I) or [None,None])[1]}); continue
        km=re.match(r'(?:UNIQUE\s+)?(?:KEY|INDEX)\s+`([^`]+)`\s*\((.*?)\)',line,re.I)
        if km:
            t['indexes'].append({'name':km.group(1),'columns':re.findall(r'`([^`]+)`',km.group(2)),'unique':line.upper().startswith('UNIQUE')}); continue
        cm=re.match(r'(?:CONSTRAINT\s+`([^`]+)`\s+)?CHECK\s*\((.*)\)',line,re.I)
        if cm: t['checks'].append({'name':cm.group(1),'expression':cm.group(2)})
    for c in t['columns']:
        c['primaryKey']=c['name'] in t['primaryKey']
        if c['primaryKey']: c['classification']['function']='Clave primaria'
    for fk in t['foreignKeys']:
        for c in t['columns']:
            if c['name'] in fk['columns']:
                c['foreignKeys'].append(fk['name']); c['classification']['function']='Clave foránea' if not c['primaryKey'] else 'Clave primaria y foránea'
    for ix in t['indexes']:
        for c in t['columns']:
            if c['name'] in ix['columns']:
                c['indexes'].append(ix['name']); c['unique'] |= ix['unique']
    for chk in t['checks']:
        for c in t['columns']:
            if f'`{c["name"]}`' in chk['expression']: c['checks'].append(chk)
    t['formalNotation']=name+'('+', '.join(c['name'] for c in t['columns'])+')'
    t['entityType']='Asociativa' if len(t['foreignKeys'])>=2 and len(t['primaryKey'])>=2 and set(t['primaryKey']).issubset({x for f in t['foreignKeys'] for x in f['columns']}) else 'Fuerte'
    tables[name]=t
# Avoid claiming row counts: dump includes updates and is not a reliable final-state reconstruction.
# Detect database objects conservatively from mysqldump wrappers.
relations=[]
for t in tables.values():
    for fk in t['foreignKeys']:
        relations.append({'name':fk['name'],'fromTable':t['name'],'fromColumns':fk['columns'],'toTable':fk['targetTable'],'toColumns':fk['targetColumns'],'explicit':True,'onDelete':fk['onDelete'],'onUpdate':fk['onUpdate'],'cardinality':'1:N (destino a origen; FK no única)','type':'Identificadora' if set(fk['columns']).issubset(t['primaryKey']) else 'No identificadora'})
for t in tables.values():
    for c in t['columns']:
        if c['foreignKeys'] and c['unique']:
            for rel in relations:
                if rel['fromTable']==t['name'] and c['name'] in rel['fromColumns']: rel['cardinality']='1:1 (FK única)'
views=re.findall(r'(?i)CREATE\s+(?:OR\s+REPLACE\s+)?VIEW\s+`([^`]+)`',src)
triggers=re.findall(r'(?i)TRIGGER\s+`([^`]+)`',src)
procedures=re.findall(r'(?i)PROCEDURE\s+`([^`]+)`',src)
functions=re.findall(r'(?i)FUNCTION\s+`([^`]+)`',src)
meta={'database':'db_test','source':'240485_27.10.26.sql','engine':'MySQL 8.0.36 / InnoDB','generated':'2026-11-06','tables':list(tables.values()),'relations':relations,'objects':{'views':views,'triggers':triggers,'procedures':procedures,'functions':functions},'counts':{'tables':len(tables),'columns':sum(len(t['columns']) for t in tables.values()),'primaryKeys':sum(bool(t['primaryKey']) for t in tables.values()),'foreignKeys':len(relations),'indexes':sum(len(t['indexes']) for t in tables.values()),'views':len(views),'triggers':len(triggers),'procedures':len(procedures),'functions':len(functions),'verifiedRows':None},'notes':['Los conteos finales de filas no se reconstruyen: hay actualizaciones posteriores a inserciones y no se ejecutó el SQL.','Descripciones funcionales y algunas clasificaciones conceptuales son inferencias de los nombres y tipos.','No se detectaron relaciones inferidas automáticamente; el diagrama muestra solo claves foráneas declaradas.']}
pathlib.Path('data').mkdir(exist_ok=True)
pathlib.Path('data/schema.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
print('tables',len(tables),'columns',meta['counts']['columns'],'fks',len(relations),'indexes',meta['counts']['indexes'],'objs',meta['objects'])
print('empty tables', [n for n,t in tables.items() if not t['columns']])
