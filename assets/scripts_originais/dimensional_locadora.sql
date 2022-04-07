-- Gerado por Oracle SQL Developer Data Modeler 20.2.0.167.1538
--   em:        2021-10-01 21:29:51 GFT
--   site:      Oracle Database 11g
--   tipo:      Oracle Database 11g



-- predefined type, no DDL - MDSYS.SDO_GEOMETRY

-- predefined type, no DDL - XMLTYPE

CREATE TABLE dm_artista (
    id_art    NUMBER(4) NOT NULL,
    tpo_art   VARCHAR2(40 BYTE) NOT NULL,
    nac_bras  VARCHAR2(40 BYTE) NOT NULL,
    nom_art   VARCHAR2(40 BYTE) NOT NULL
);

ALTER TABLE dm_artista ADD CHECK ( cod_art > 0 );

ALTER TABLE dm_artista
    ADD CHECK ( tpo_art IN ( 'B', 'D', 'I' ) );

ALTER TABLE dm_artista
    ADD CHECK ( nac_bras IN ( 'F', 'V' ) );

ALTER TABLE dm_artista ADD CONSTRAINT dm_artistas_pk PRIMARY KEY ( id_art );

CREATE TABLE dm_gravadora (
    id_grav   NUMBER(4) NOT NULL,
    uf_grav   VARCHAR2(50 BYTE) NOT NULL,
    nac_bras  VARCHAR2(30 BYTE) NOT NULL,
    nom_grav  VARCHAR2(40 BYTE) NOT NULL
);

ALTER TABLE dm_gravadora ADD CHECK ( cod_grav > 0 );

ALTER TABLE dm_gravadora
    ADD CHECK ( uf_grav IN ( 'AC', 'AL', 'AM', 'BA', 'CE',
                             'DF', 'ES', 'GO', 'MA', 'MG',
                             'MS', 'MT', 'PA', 'PB', 'PE',
                             'PI', 'PR', 'RJ', 'RN',
                             'RO',
                             'RR',
                             'RS',
                             'SC',
                             'SE',
                             'SP',
                             'TO' ) );

ALTER TABLE dm_gravadora
    ADD CHECK ( nac_bras IN ( 'F', 'V' ) );

ALTER TABLE dm_gravadora ADD CONSTRAINT dm_gravadora_pk PRIMARY KEY ( id_grav );

CREATE TABLE dm_socio (
    id_soc      NUMBER(4) NOT NULL,
    nom_soc     VARCHAR2(40 BYTE) NOT NULL,
    tipo_socio  VARCHAR2(40 BYTE) NOT NULL
);

ALTER TABLE dm_socio ADD CHECK ( cod_soc > 0 );

ALTER TABLE dm_socio ADD CONSTRAINT dm_socios_pk PRIMARY KEY ( id_soc );

CREATE TABLE dm_tempo (
    id_tempo   NUMBER(6) NOT NULL,
    nu_ano     NUMBER(4) NOT NULL,
    nu_mes     NUMBER(2) NOT NULL,
    nu_anomes  NUMBER(7) NOT NULL,
    sg_mes     CHAR(3) NOT NULL,
    nm_mesano  CHAR(8) NOT NULL,
    nm_mes     VARCHAR2(15) NOT NULL,
    nu_dia     NUMBER(2) NOT NULL,
    dt_tempo   DATE NOT NULL,
    nu_hora    NUMBER(02) NOT NULL,
    turno      VARCHAR2(30) NOT NULL
);

ALTER TABLE dm_tempo ADD CONSTRAINT dm_tempo_pk PRIMARY KEY ( id_tempo );

CREATE TABLE dm_titulo (
    id_titulo   NUMBER(6) NOT NULL,
    tpo_titulo  VARCHAR2(40 BYTE) NOT NULL,
    cla_titulo  VARCHAR2(40 BYTE) NOT NULL,
    dsc_titulo  VARCHAR2(40 BYTE) NOT NULL
);

ALTER TABLE dm_titulo ADD CHECK ( cod_tit > 0 );

ALTER TABLE dm_titulo
    ADD CHECK ( tpo_titulo IN ( 'C', 'D' ) );

ALTER TABLE dm_titulo
    ADD CHECK ( cla_titulo IN ( 'L', 'N', 'P' ) );

ALTER TABLE dm_titulo ADD CONSTRAINT dm_titulos_pk PRIMARY KEY ( id_titulo );

CREATE TABLE ft_locacoes (
    id_soc            NUMBER(4) NOT NULL,
    id_titulo         NUMBER(6) NOT NULL,
    id_art            NUMBER(4) NOT NULL,
    id_grav           NUMBER(4) NOT NULL,
    id_tempo          NUMBER(6) NOT NULL,
    valor_arrecadado  NUMBER(10, 2) NOT NULL,
    tempo_devolucao   NUMBER(10, 2) NOT NULL,
    multa_atraso      NUMBER(10, 2) NOT NULL
);

ALTER TABLE ft_locacoes ADD CHECK ( cod_soc > 0 );

ALTER TABLE ft_locacoes ADD CHECK ( cod_tit > 0 );

ALTER TABLE ft_locacoes ADD CHECK ( cod_art > 0 );

ALTER TABLE ft_locacoes ADD CHECK ( cod_grav > 0 );

ALTER TABLE ft_locacoes ADD CHECK ( val_loc > 0 );

ALTER TABLE ft_locacoes ADD CHECK ( val_loc > 0 );

ALTER TABLE ft_locacoes ADD CHECK ( val_loc > 0 );

ALTER TABLE ft_locacoes
    ADD CONSTRAINT ft_locacoes_pk PRIMARY KEY ( id_soc,
                                                id_titulo,
                                                id_art,
                                                id_grav,
                                                id_tempo );

ALTER TABLE ft_locacoes
    ADD CONSTRAINT ft_locacoes_dm_artista_fk FOREIGN KEY ( id_art )
        REFERENCES dm_artista ( id_art );

ALTER TABLE ft_locacoes
    ADD CONSTRAINT ft_locacoes_dm_gravadora_fk FOREIGN KEY ( id_grav )
        REFERENCES dm_gravadora ( id_grav );

ALTER TABLE ft_locacoes
    ADD CONSTRAINT ft_locacoes_dm_socio_fk FOREIGN KEY ( id_soc )
        REFERENCES dm_socio ( id_soc );

ALTER TABLE ft_locacoes
    ADD CONSTRAINT ft_locacoes_dm_tempo_fk FOREIGN KEY ( id_tempo )
        REFERENCES dm_tempo ( id_tempo );

ALTER TABLE ft_locacoes
    ADD CONSTRAINT ft_locacoes_dm_titulo_fk FOREIGN KEY ( id_titulo )
        REFERENCES dm_titulo ( id_titulo );



-- Relatório do Resumo do Oracle SQL Developer Data Modeler: 
-- 
-- CREATE TABLE                             6
-- CREATE INDEX                             0
-- ALTER TABLE                             28
-- CREATE VIEW                              0
-- ALTER VIEW                               0
-- CREATE PACKAGE                           0
-- CREATE PACKAGE BODY                      0
-- CREATE PROCEDURE                         0
-- CREATE FUNCTION                          0
-- CREATE TRIGGER                           0
-- ALTER TRIGGER                            0
-- CREATE COLLECTION TYPE                   0
-- CREATE STRUCTURED TYPE                   0
-- CREATE STRUCTURED TYPE BODY              0
-- CREATE CLUSTER                           0
-- CREATE CONTEXT                           0
-- CREATE DATABASE                          0
-- CREATE DIMENSION                         0
-- CREATE DIRECTORY                         0
-- CREATE DISK GROUP                        0
-- CREATE ROLE                              0
-- CREATE ROLLBACK SEGMENT                  0
-- CREATE SEQUENCE                          0
-- CREATE MATERIALIZED VIEW                 0
-- CREATE MATERIALIZED VIEW LOG             0
-- CREATE SYNONYM                           0
-- CREATE TABLESPACE                        0
-- CREATE USER                              0
-- 
-- DROP TABLESPACE                          0
-- DROP DATABASE                            0
-- 
-- REDACTION POLICY                         0
-- 
-- ORDS DROP SCHEMA                         0
-- ORDS ENABLE SCHEMA                       0
-- ORDS ENABLE OBJECT                       0
-- 
-- ERRORS                                   0
-- WARNINGS                                 0
