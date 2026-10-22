try:
    import pymysql
    from django.db.backends.base.base import BaseDatabaseWrapper
    from django.db.backends.mysql.features import DatabaseFeatures

    # Enable PyMySQL as MySQLdb if using MySQL
    pymysql.install_as_MySQLdb()

    # Compatibility patches for MariaDB 10.4.x (common in XAMPP on Windows)
    BaseDatabaseWrapper.check_database_version_supported = lambda self: None
    DatabaseFeatures.can_return_columns_from_insert = False
    DatabaseFeatures.can_return_rows_from_bulk_insert = False
except Exception:
    pass

