from commands import Commands


class LiteORM:

    db = None

    def __init__(self, model: object, connection_params: dict = None):
        if connection_params:
            if 'user' in connection_params:
                import mysql.connector
                LiteORM.db = mysql.connector.connect(**connection_params)
            else:
                import sqlite3
                LiteORM.db = sqlite3.connect(
                    connection_params['database'],
                    check_same_thread=False
                )
        self.model = model
        self.cmds = Commands(self.model).sql
        self._execute('create')

    def _execute(self, _type: str, cmds: dict = None, obj: object = None):
        cursor = LiteORM.db.cursor()
        cursor.execute((cmds or self.cmds)[_type])
        if _type == 'select':
            dataset = cursor.fetchall()
            model = obj or self.model
            return [model.__class__(
                **{k: v for k, v in zip(model.__dict__, row)}
            ) for row in dataset]
        LiteORM.db.commit()

    @classmethod
    def find(cls, model: object):
        """
        Finds records whose fields match conditions in the model properties

        Example:
        ---
        > find(
            User(
                name='LIKE "Jo%"',
                age='> 18',
                department='IN (1, 2, 3)',
                status='= 1'
            )
        )
        """
        return cls._execute(
            'select',
            Commands(
                model,
                conditions=[f'{k} {v}' for k, v in model.__dict__.items() if v]
            ).sql,
            model
        )

    def save(self):  # Upsert
        self.cmds = Commands(self.model)
        found = self._execute('select')
        if not found:
            return self._execute('insert')
        d1, d2 = found[0].__dict__, self.model.__dict__
        differences = {k: v for k, v in d1.items() if v != d2.get(k)}
        if differences:
            return self._execute('update')
        return None

    def delete(self):
        self._execute('delete')
