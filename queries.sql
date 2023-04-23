CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    region_name VARCHAR(255) NOT NULL,
    datetime_epoch TIMESTAMP NOT NULL,
    prediction INTEGER NOT NULL,
    CONSTRAINT unique_region_datetime UNIQUE (region_name, datetime_epoch)
);

CREATE TABLE models (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    model_name VARCHAR(255) NOT NULL,
    model_file BYTEA NOT NULL
);

CREATE TABLE vector (
  id SERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT NOW(),
  words_vector VARCHAR[] NOT NULL
);

INSERT INTO vector (words_vector)
VALUES (ARRAY['apple', 'banana', 'cherry']::varchar[]);
