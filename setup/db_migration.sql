BEGIN;

SET FOREIGN_KEY_CHECKS=0;

-- CHACARA
alter table Chacara
    modify chac_ID smallint(6) unsigned;

alter table Visitante
    modify chac_ID smallint(6) unsigned,
    modify veic_ID varchar(7) null;

alter table Residente
    drop primary key,
    modify chac_ID smallint(6) unsigned null;

alter table Chacara engine=innodb;

-- VISITANTE
alter table Visitante engine=innodb;

alter table Visitante
  add column (
  Agendado  tinyint(1)             not null,
  data      date                   null),

  add constraint Visitante_chac_ID_1c276e81_fk_Chacara_chac_ID
  foreign key (chac_ID) references Chacara (chac_ID);

create index Visitante_chac_ID_1c276e81
  on Visitante (chac_ID);

-- MOVIMENTO
alter table Movimento engine=innodb;

alter table Movimento
  add constraint Movimento_vis_ID_cc77c620_fk_Visitante_vis_ID
  foreign key (vis_ID) references Visitante (vis_ID);

create index Movimento_vis_ID_cc77c620
  on Movimento (vis_ID);

-- RESIDENTE
alter table Residente engine=innodb;

alter table Residente
  modify nome varchar(50) null,

  add column (
  id           int auto_increment primary key,
  password     varchar(128) not null,
  last_login   datetime(6)  null,
  is_superuser tinyint(1)   not null,
  token        varchar(8)   null,
  email        varchar(254) null,
  date_joined  datetime(6)  null,
  is_staff     tinyint(1)   not null,
  is_active    tinyint(1)   not null),

  add constraint Residente_chac_id_nome_ebf9b42a_uniq
  unique (chac_id, nome),

  add constraint email
  unique (email),

  add constraint token
  unique (token),

  add constraint Residente_chac_id_ef9266f2_fk_Chacara_chac_ID
  foreign key (chac_id) references Chacara (chac_ID);

create index Residente_chac_id_ef9266f2
  on Residente (chac_id);


-- CREATING TABLES
-- auth_group
create table auth_group
(
  id   int auto_increment
    primary key,
  name varchar(80) not null,
  constraint name
  unique (name)
);

-- django_content_type
create table django_content_type
(
  id        int auto_increment
    primary key,
  app_label varchar(100) not null,
  model     varchar(100) not null,
  constraint django_content_type_app_label_model_76bd3d3b_uniq
  unique (app_label, model)
);

-- django_session
create table django_session
(
  session_key  varchar(40) not null
    primary key,
  session_data longtext    not null,
  expire_date  datetime(6) not null
);
create index django_session_expire_date_a5c62663
  on django_session (expire_date);

-- auth_permission
create table auth_permission
(
  id              int auto_increment
    primary key,
  name            varchar(255) not null,
  content_type_id int          not null,
  codename        varchar(100) not null,
  constraint auth_permission_content_type_id_codename_01ab375a_uniq
  unique (content_type_id, codename),
  constraint auth_permission_content_type_id_2f476e4b_fk_django_co
  foreign key (content_type_id) references django_content_type (id)
);

-- auth_group_permissions
create table auth_group_permissions
(
  id            int auto_increment
    primary key,
  group_id      int not null,
  permission_id int not null,
  constraint auth_group_permissions_group_id_permission_id_0cd325b0_uniq
  unique (group_id, permission_id),
  constraint auth_group_permissio_permission_id_84c5c92e_fk_auth_perm
  foreign key (permission_id) references auth_permission (id),
  constraint auth_group_permissions_group_id_b120cbf9_fk_auth_group_id
  foreign key (group_id) references auth_group (id)
);


-- Criando tabelas para depois definir os foreigns keys
-- Residente_groups
create table Residente_groups
(
  id           int auto_increment
    primary key,
  residente_id int not null,
  group_id     int not null,

  constraint Residente_groups_residente_id_group_id_3ee20c17_uniq
  unique (residente_id, group_id)
);

-- Residente_user_permissions
create table Residente_user_permissions
(
  id            int auto_increment
    primary key,
  residente_id  int not null,
  permission_id int not null,

  constraint Residente_user_permissio_residente_id_permission__6e226175_uniq
  unique (residente_id, permission_id)
);

-- django_admin_log
create table django_admin_log
(
  id              int auto_increment
    primary key,
  action_time     datetime(6)          not null,
  object_id       longtext             null,
  object_repr     varchar(200)         not null,
  action_flag     smallint(5) unsigned not null,
  change_message  longtext             not null,
  content_type_id int                  null,
  user_id         int                  not null
);

-- Definindo foreign keys
-- Residente_user_permissions
alter table Residente_user_permissions
  add constraint Residente_user_permi_permission_id_4b48fc7a_fk_auth_perm
  foreign key (permission_id) references auth_permission (id);

-- Residente_groups
alter table Residente_groups
  add constraint Residente_groups_group_id_7df51cd1_fk_auth_group_id
  foreign key (group_id) references auth_group (id);

-- django_admin_log
alter table django_admin_log
  add constraint django_admin_log_content_type_id_c4bce8eb_fk_django_co
  foreign key (content_type_id) references django_content_type (id);


-- Definindo foreign keys com o Residente
-- Residente_user_permissions
alter table Residente_user_permissions
  add constraint Residente_user_permissions_residente_id_be3240d1_fk_Residente_id
  foreign key (residente_id) references Residente (id);

-- Residente_groups
alter table Residente_groups
  add constraint Residente_groups_residente_id_8f70e3e9_fk_Residente_id
  foreign key (residente_id) references Residente (id);

-- django_admin_log
alter table django_admin_log
  add constraint django_admin_log_user_id_c564eba6_fk_Residente_id
  foreign key (user_id) references Residente (id);

SET FOREIGN_KEY_CHECKS=1;

COMMIT;