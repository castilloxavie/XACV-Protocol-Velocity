use car_game_db;

/*REGISTRO DE USUARIOS*/
drop procedure if exists sp_registrar_usuario;

DELIMITER $$

create procedure sp_registrar_usuario(
	in p_usermane varchar(30),
    in p_email varchar(120),
    in p_password_hash varchar(255),
    in p_salt varchar(255),
    in p_ip varchar(45),
    out p_resultado int,
    out p_mensaje varchar(255)
)
begin
	declare v_existe_user int default 0;
    declare v_existe_email int default 0;
    declare v_nuevo_id bigint unsigned;
    
    declare exit handler for sqlexception
    begin
		rollback;
        set p_resultado = -99;
        set p_mensaje = 'Error interno de la base de datos';
	end;
    
    start transaction;
    
    if p_usermane is null or char_length(p_usermane) < 3 or char_length(p_usermane) > 30 then
		set p_resultado = -1;
        set p_mensaje = 'El nombre del usuario debe de tener entre 3 y 30 caracteres';
        rollback;
        
	elseif p_email is null or p_email not like '%_@_%.__%' then
		set p_resultado = -2;
        set p_mensaje = 'El correo electronico con formato invalido';
        rollback;
        
	elseif p_password_hash is null or char_length(p_password_hash) < 20 then
		set p_resultado = -3;
        set p_mensaje = 'Hash de contraseña invalido';
        rollback;
        
	else
		select count(*) into v_existe_user from usuarios where username = p_usermane;
        select count(*) into v_existe_email from usuarios where email = p_email;
        
        if v_existe_user > 0 then
			set p_resultado = -4;
            set p_mensaje = 'El nombre del usuario ya esta en uso';
            rollback;
            
		elseif v_existe_email > 0 then
			set p_resultado = -5;
            set p_mensaje = 'El correo electronico ya está registrado';
            rollback;
            
		else
			insert into usuarios (username, email, password_hash, salt)
            values (p_usermane, p_email, p_password_hash, p_salt);
            
            set v_nuevo_id = last_insert_id();
            
            insert into estadisticas_usuario(id_usuario) values(v_nuevo_id);
            
            insert into auditoria_seguridad (tipo_evento, id_usuario, descripcion, ip_origen)
            values('Registro_Exitoso', v_nuevo_id, concat('Nuevo usuario registrado: ', p_usermane), p_ip);
            
            commit;
            set p_resultado = 1;
            set p_mensaje = concat('Usuario registrado correctamente. ID= ', v_nuevo_id);
		end if;
	end if;
end $$
DELIMITER ;


/*INICIAR LOGUIN (SOLO CONSULTA)*/
DROP PROCEDURE IF EXISTS sp_iniciar_login;
DELIMITER $$

CREATE PROCEDURE sp_iniciar_login(
    IN  p_username        VARCHAR(30),
    OUT p_resultado       INT,
    OUT p_mensaje         VARCHAR(255),
    OUT p_id_usuario      BIGINT UNSIGNED,
    OUT p_password_hash   VARCHAR(255),
    OUT p_salt            VARCHAR(64),
    OUT p_bloqueado_hasta DATETIME,
    OUT p_rol             VARCHAR(20)  -- NUEVO PARÁMETRO
)
BEGIN
    DECLARE v_existe    INT DEFAULT 0;
    DECLARE v_activo    BOOLEAN DEFAULT FALSE;
    DECLARE v_bloqueado DATETIME DEFAULT NULL;

    SET p_id_usuario      = NULL;
    SET p_password_hash   = NULL;
    SET p_salt            = NULL;
    SET p_bloqueado_hasta = NULL;
    SET p_rol             = NULL;

    SELECT COUNT(*), MAX(activo), MAX(bloqueado_hasta), MAX(id_usuario), MAX(rol)
      INTO v_existe, v_activo, v_bloqueado, p_id_usuario, p_rol
      FROM usuarios WHERE username = p_username;

    IF v_existe = 0 THEN
        SET p_resultado = -1; SET p_mensaje = 'Credenciales inválidas';
    ELSEIF v_activo = FALSE THEN
        SET p_resultado = -2; SET p_mensaje = 'Cuenta desactivada';
    ELSEIF v_bloqueado IS NOT NULL AND v_bloqueado > NOW() THEN
        SET p_bloqueado_hasta = v_bloqueado;
        SET p_resultado = -3;
        SET p_mensaje = CONCAT('Cuenta bloqueada hasta ', DATE_FORMAT(v_bloqueado, '%H:%i:%s'));
    ELSE
        SELECT password_hash, salt INTO p_password_hash, p_salt FROM usuarios WHERE id_usuario = p_id_usuario;
        SET p_resultado = 0; SET p_mensaje = 'OK';
    END IF;
END$$
DELIMITER ;



/*REGISTRA LOS RESULTADOS DEL LOGION(EXITOSOS, FALLIDOS + EL BLOQUEO)*/
drop procedure if exists sp_guardar_puntuacion;
DELIMITER $$

create procedure sp_guardar_puntuacion(
    in p_id_usuario bigint unsigned,
    in p_puntuacion int unsigned,
    in p_nivel_velocidad tinyint unsigned,
    in p_duracion_segundos int unsigned,
    in p_carros_rebasados int unsigned,
    in p_ip varchar(45),
    out p_resultado int,
    out p_mensaje varchar(255),
    out p_es_record boolean
)
begin
    declare v_max_plausible int unsigned;
    declare v_mejor_actual int unsigned default 0;
    declare v_existe_user int default 0;
    
    declare exit handler for sqlexception
    begin
        rollback;
        set p_resultado = -99;
        set p_mensaje = 'error interno al guardar puntuación';
    end;

    set p_es_record = false;

    start transaction;

    select count(*) into v_existe_user
      from usuarios
     where id_usuario = p_id_usuario and activo = true;

    if v_existe_user = 0 then
        set p_resultado = -2;
        set p_mensaje = 'usuario inválido o inactivo';
        rollback;
    else
        set v_max_plausible = greatest(p_duracion_segundos * 60, 500);

        if p_puntuacion > v_max_plausible then
            insert into auditoria_seguridad (tipo_evento, id_usuario, descripcion, ip_origen)
            values ('score_sospechoso', p_id_usuario, concat('score=', p_puntuacion, ' duración=', p_duracion_segundos, 's maxesperado=', v_max_plausible), p_ip);

            set p_resultado = -1;
            set p_mensaje = 'puntuación no plausible para la duración de la partida';
            rollback;
        else
            insert into partidas
                (id_usuario, puntuacion, nivel_velocidad,
                 duracion_segundos, carros_rebasados, ip_origen)
            values
                (p_id_usuario, p_puntuacion, p_nivel_velocidad,
                 p_duracion_segundos, p_carros_rebasados, p_ip);

            select mejor_puntuacion into v_mejor_actual
              from estadisticas_usuario
             where id_usuario = p_id_usuario
             for update;

            if p_puntuacion > v_mejor_actual then
                set p_es_record = true;
            end if;

            update estadisticas_usuario
               set mejor_puntuacion = greatest(mejor_puntuacion, p_puntuacion),
                   total_partidas   = total_partidas + 1,
                   total_rebasados  = total_rebasados + p_carros_rebasados,
                   tiempo_total_seg = tiempo_total_seg + p_duracion_segundos,
                   ultima_partida   = now()
             where id_usuario = p_id_usuario;

            commit;
            set p_resultado = 1;
            set p_mensaje   = if(p_es_record, '¡nuevo récord personal!', 'puntuación guardada');
        end if;
    end if;
end$$
DELIMITER ;




/*ESTADISTICAS DE USUARIO*/
drop procedure if exists sp_obtener_estadisticas_usuario;

DELIMITER $$
create procedure sp_obtener_estadisticas_usuario (
	in p_id_usuario bigint unsigned,
    out p_resultado int,
    out p_mensaje varchar(255)
)
begin
	select 
		u.username,
        u.fecha_registro,
        u.ultimo_loguin,
        e.mejor_puntuacion,
        e.total_partidas,
        e.total_rebasadas,
        e.tiempo_total_segundo,
        e.ultima_partida
    from usuarios u
		left join estadisticas_usuario e on e.id_usuario = u.id_usuario
    where u.id_usuario = p_id_usuario;
    
    set p_resultado = 1;
    set p_mensaje = 'Ok';
end$$
DELIMITER ;



/*RANKING GLOBAL (TOP 10)*/
drop procedure if exists sp_obtener_ranking_global;

DELIMITER $$

create procedure sp_obtener_ranking_global(
	in p_limite tinyint unsigned
)
begin
	set p_limite = least(greatest(ifnull(p_limite, 10), 1), 50);
    
    select 
		u.username,
        e.mejor_puntuacion,
        e.total_partidas,
        e.total_rebasadas
    from estadisticas_usuario e
		join usuarios u on u.id_usuario = e.id_usuario
    where u.activo = true
    order by e.mejor_puntuacion desc, e.total_rebasadas desc
    limit p_limite;
end$$
DELIMITER ;


/*HISTORIAL DE PARTIDAS*/
drop procedure if exists sp_obtener_historial_partidas;

DELIMITER $$

create procedure sp_obtener_historial_partidas(
	in p_id_usuario bigint unsigned,
    in p_limite tinyint unsigned
)
begin 
	set p_limite = least(greatest(ifnull(p_limite, 20), 1), 100);
    
    select 
		id_partida,
        puntuacion,
        nivel_velocidad,
        duracion_segundos,
        carros_rebasados,
        fecha_partida
    from partidas
    where id_usuario = p_id_usuario
    order by fecha_partida desc
    limit p_limite;
end$$
DELIMITER ;



/*AUDITORIA DE EVENTOS*/
drop procedure if exists sp_auditar_evento;

DELIMITER $$

create procedure sp_auditar_evento(
	in p_tipo_evento varchar(50),
    in p_id_usuario bigint unsigned,
    in p_descripcion varchar(500),
    in p_ip varchar(45)
)
begin
	insert into auditoria_seguridad (tipo_evento, id_usuario, descripcion, ip_origen)
    values(left(p_tipo_evento, 50), p_id_usuario, left(p_descripcion, 500), left(p_ip, 45));
end$$
DELIMITER ;
    