class Commands:
    templates = {
        'delete': 'DELETE FROM {table} WHERE {key}={value}',
        'insert': 'INSERT INTO {table}({fields}) VALUES({insert_values})',
        'update': 'UPDATE {table} SET {udpate_values} WHERE {key}={value}',
        'select': 'SELECT {fields} FROM {table} WHERE {key}={value}',
        'create': 'CREATE TABLE IF NOT EXISTS {table}({schema})'
    }

    def __init__(self, obj: object, key: str = 'id'):
        def format_value(var):
            if isinstance(var, str):
                return 'text', f'"{var}"'
            return var.__class__.__name__, str(var)
        schema = {f: format_value(v) for f, v in obj.__dict__.items()}
        data = dict(
            table=obj.__class__.__name__,
            key=key,
            value=format_value(obj.__dict__[key])[1],
            schema=','.join('{} {}{}'.format(
                    f, v[0], ' PRIMARY KEY' if f == key else ''
                )
                for f, v in schema.items()
            ),
            insert_values=','.join(v[1] for v in schema.values()),
            udpate_values=','.join(
                f'{f}={v[1]}' for f, v in schema.items()
                if f != key
            ),
            fields=','.join(schema),
        )
        self.sql = {k: v.format(**data) for k, v in self.templates.items()}
