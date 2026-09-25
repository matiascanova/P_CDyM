CREATE TABLE categoria(
    id int NOT NULL,
    nombre varchar NOT NULL,
    ADD CONSTRAINT  categoria_pk PRIMARY KEY (id)
);

CREATE TABLE gasto(
    id int NOT NULL,
    monto int NOT NULL,
    fecha date NOT NULL,
    categoria_id int NOT NULL,
    ADD CONSTRAINT  gasto_pk PRIMARY KEY (id)
);

ALTER TABLE gasto ADD CONSTRAINT gasto_fk 
FOREIGN KEY categoria_id REFERENCES categoria (id)
ON DELETE RESTRICT
ON UPDATE CASCADE
;