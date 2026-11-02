create database if not exists car_game_db
character set utf8mb4
collate utf8mb4_0900_ai_ci;

use car_game_db;

create table if not exists usuarios (
	id_usuario bigint unsigned auto_increment primary key,
    username varchar(30) not null unique,
    email varchar(120) not null unique,
    password_hash varchar(255) not null,
    salt varchar(255) not null,
    fecha_registro datetime not null default current_timestamp,
    ultimo_login datetime null,
    intentos_fallidos tinyint unsigned not null default 0,
    bloqueado_hasta datetime null,
    activo boolean not null default true,
    rol enum('jugador', 'admin') not null default 'jugador',
    constraint chk_username_len check (char_length(username) between 3 and 30),
    constraint chk_email_len check(char_length(email) between 5 and 30)
) engine=InnoDB;

create table if not exists partidas (
	id_partida bigint unsigned auto_increment primary key,
    id_usuario bigint unsigned not null,
    puntuacion int unsigned not null,
    nivel_velocidad tinyint unsigned not null,
    duracion_segundos int unsigned not null,
    carros_rebasados int unsigned not null default 0,
    fecha_partida datetime not null default current_timestamp,
    ip_origen varchar(45) null,
    constraint fk_partidas_usuario foreign key (id_usuario) references usuarios(id_usuario) on delete cascade,
    constraint chk_duracion check (duracion_segundos  > 0 and duracion_segundos  < 86400 )
) engine=InnoDB;

create index idx_partidas_usuario on partidas(id_usuario, fecha_partida desc);
create index idx_partidas_score on partidas(puntuacion);

create table if not exists estadisticas_usuario (
	id_usuario bigint unsigned primary key,
    mejor_puntuacion int unsigned not null default 0,
    total_partidas int unsigned not null default 0,
    total_rebasadas int unsigned not null default 0,
    tiempo_total_segundo int unsigned not null default 0,
    ultima_partida datetime null,
    constraint fk_estadisticas_usuario foreign key (id_usuario) references usuarios (id_usuario) on delete cascade
)engine=InnoDB;

create table if not exists registro_intentos_login (
	id_intentos bigint unsigned auto_increment primary key,
    username_intentado varchar(30) not null,
    exito boolean not null,
    ip_origen varchar(45) null,
    user_agent varchar(255) null,
    fecha_intento datetime not null default current_timestamp
)engine=InnoDB;

create index idx_intentos_username on registro_intentos_login(username_intentado, fecha_intento desc);

create table if not exists auditoria_seguridad (
	id_evento bigint unsigned auto_increment primary key,
    tipo_evento varchar(50) not null,
    id_usuario bigint unsigned null,
    descripcion text null,
    fecha_evento datetime not null default current_timestamp,
    constraint fk_auditoria_usuario foreign key (id_usuario) references usuarios(id_usuario) on delete cascade
)engine=InnoDB;

create index idx_auditoria_tipo  on auditoria_seguridad(tipo_evento, fecha_evento desc);

alter table auditoria_seguridad
add column  ip_origen varchar(45) null after descripcion;


