create table if not exists users
(
    id         bigserial   not null primary key,
    name       varchar     not null,              -- Имя
    about      text        not null,              -- Описание
    avatar     varchar     not null,              -- Ссылка на аватар
    cohort     varchar     not null,              -- Группа
    token      varchar     not null,              -- Токен авторизации
    is_active  boolean     not null default true  -- Активность
);

create table if not exists cards
(
    id         bigserial                  not null primary key,
    cohort     varchar                    not null,                -- Группа
    name       varchar                    not null,                -- Название
    link       varchar                    not null,                -- Ссылка на фото
    owner_id   bigint                     not null,                -- ID владельца
    is_active  boolean                    not null default true,   -- Активность
    created_at timestamp with time zone   not null,                -- Дата создания
    updated_at timestamp with time zone   not null,                -- Дата обновления
    constraint cards_owner_id_fk foreign key(owner_id) references users(id)
);

create table if not exists likes
(
    user_id     bigint                      not null,                -- ID пользователя
    card_id     bigint                      not null,                -- ID карточки
    is_active   boolean                     not null default true,   -- Активность
    created_at  timestamp with time zone    not null,                -- Дата создания
    updated_at  timestamp with time zone    not null,                -- Дата обновления
    constraint likes_pk primary key (user_id, card_id),              -- Составной первичный ключ
    constraint likes_user_id_fk foreign key(user_id) references users(id),
    constraint likes_card_id_fk foreign key(card_id) references cards(id)
);
