import psycopg2

from constants import DB_NAME, DB_USER, DB_PASS, DB_HOST, DB_PORT

conn = psycopg2.connect(database=DB_NAME,
                        user=DB_USER,
                        password=DB_PASS,
                        host=DB_HOST,
                        port=DB_PORT)
print("Database connected successfully")

cur = conn.cursor()  # creating a cursor

def create_tables():
    cur.execute(
        '''
        CREATE TABLE ExperimentParams (
            eid INTEGER PRIMARY KEY,
            town_size INTEGER NOT NULL,
            exp_daily_lightning INTEGER NOT NULL,
            max_days INTEGER NOT NULL
        );

        CREATE TABLE Samples (
            id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            eid INTEGER REFERENCES ExperimentParams (eid),
            survived BOOLEAN NOT NULL,
            total_days INTEGER NOT NULL,
            survival_day INTEGER NOT NULL,
            total_assets INTEGER NOT NULL,
            num_of_destroyed INTEGER NOT NULL
        );

        CREATE TABLE Assets (
            sid INTEGER REFERENCES Samples (id),
            atype VARCHAR(1) NOT NULL,
            a_row INTEGER NOT NULL,
            a_col INTEGER NOT NULL,
            importance INTEGER NOT NULL,
            destroyed BOOLEAN NOT NULL,
            PRIMARY KEY (sid, atype, a_row, a_col)
        );

        CREATE TABLE LightningStrikes (
            sid INTEGER REFERENCES Samples (id),
            day INTEGER NOT NULL,
            num_of_strikes INTEGER NOT NULL,
            PRIMARY KEY (sid, day)
        );
        '''
    )
    conn.commit()
    print("Tables created successfully")

def reset_db():
    cur.execute(
        '''
        DROP TABLE IF EXISTS LightningStrikes;
        DROP TABLE IF EXISTS Assets;
        DROP TABLE IF EXISTS Samples;
        DROP TABLE IF EXISTS ExperimentParams;
        '''
    )
    conn.commit()
    print("Tables dropped successfully")
    create_tables()

def add_experiment_params_if_not_exist(id, town_size, exp_daily_lightning, max_days):
    # First, check if a matching row exists
    cur.execute(
        '''
        SELECT eid 
        FROM ExperimentParams 
        WHERE town_size = %s 
          AND exp_daily_lightning = %s 
          AND max_days = %s;
        ''',
        (town_size, exp_daily_lightning, max_days)
    )
    
    existing = cur.fetchone()
    
    if existing:
        return existing[0]
    else:
        cur.execute(
            '''
            INSERT INTO ExperimentParams (eid, town_size, exp_daily_lightning, max_days)
            VALUES (%s, %s, %s, %s)
            RETURNING eid;
            ''',
            (id, town_size, exp_daily_lightning, max_days)
        )
        conn.commit()
        eid = cur.fetchone()[0]
        return eid

def add_sample(eid, survived, total_days, survival_day, total_assets, num_of_destroyed):
    cur.execute(
        '''
        INSERT INTO Samples (eid, survived, total_days, survival_day, total_assets, num_of_destroyed)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id;
        ''',
        (eid, survived, total_days, survival_day, total_assets, num_of_destroyed)
    )
    conn.commit()
    sample_id = cur.fetchone()[0]
    return sample_id

def add_asset(sample_id, atype, a_row, a_col, importance, destroyed):
    cur.execute(
        '''
        INSERT INTO Assets (sid, atype, a_row, a_col, importance, destroyed)
        VALUES (%s, %s, %s, %s, %s, %s);
        ''',
        (sample_id, atype, a_row, a_col, importance, destroyed)
    )  
    conn.commit()

def add_lightning_strike(sample_id, day, num_of_strikes):
    cur.execute(
        '''
        INSERT INTO LightningStrikes (sid, day, num_of_strikes)
        VALUES (%s, %s, %s);
        ''',
        (sample_id, day, num_of_strikes)
    )
    conn.commit()

def create_real_lightning_data_table():
    cur.execute(
        '''
        CREATE TABLE LightningData (
            lid INTEGER GENERATED ALWAYS AS IDENTITY,
            datetime DATE NOT NULL,
            l_type VARCHAR(1) NOT NULL,
            latitude DECIMAL NOT NULL,
            longitude DECIMAL NOT NULL
        )
        '''
    )
    conn.commit()
    print("LightningData table created successfully")

def add_real_lightning_data(date, type, latitude, longitude):
    cur.execute(
        '''
        SELECT lid 
        FROM LightningData 
        WHERE datetime = %s 
          AND l_type = %s 
          AND latitude = %s
          AND longitude = %s;
        ''',
        (date, type, latitude, longitude)
    )
    
    existing = cur.fetchone()
    
    if existing:
        print("Real lightning data record already exists", date, type, latitude, longitude)
        return
    
    cur.execute(
        '''
        INSERT INTO LightningData (datetime, l_type, latitude, longitude)
        VALUES (%s, %s, %s, %s);
        ''',
        (date, type, latitude, longitude)
    )
    conn.commit()
    print("Successfully added real lightning data record", date, type, latitude, longitude)