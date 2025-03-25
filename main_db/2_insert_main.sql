-- Вставляем пользователей
INSERT INTO users (
        uuid,
        email,
        passwd_hash,
        first_name,
        last_name,
        telephone,
        city,
        about,
        verified
    )
SELECT '',
    format('user%s@example.com', i),
    'hashed_password' || i,
    ('Имя' || i),
    ('Фамилия' || i),
    format('+7%010s', (random() * 9999999999)::bigint),
    ('Город' || (1 + random() * 5)::int),
    'Описание пользователя',
    (random() > 0.5)
FROM generate_series(1, 50) AS i;
-- Вставляем организации
INSERT INTO orgs (
        uuid,
        email,
        passwd_hash,
        name,
        rating,
        type,
        city,
        address,
        telephone,
        lat,
        long,
        about,
        verified
    )
SELECT '',
    format('org%s@example.com', i),
    'hashed_password' || i,
    ('Организация' || i),
    round((random() * 5)::numeric, 1),
    CASE
        (i % 3)
        WHEN 0 THEN 'pharmacy'
        WHEN 1 THEN 'gym'
        ELSE 'education'
    END,
    ('Город' || (1 + random() * 5)::int),
    ('Улица ' || i),
    format('+7%010s', (random() * 9999999999)::bigint),
    50 + random() * 10,
    30 + random() * 10,
    'Описание организации',
    (random() > 0.3)
FROM generate_series(1, 10) AS i;
-- Вставляем услуги для организаций
INSERT INTO services (org_id, name, cost, description)
SELECT o.org_id,
    ('Услуга ' || j || ' организации ' || o.org_id),
    round((random() * 2000 + 500)::numeric, 2),
    'Описание услуги'
FROM orgs o,
    generate_series(1, 5) AS j;
-- Вставляем сотрудников
INSERT INTO workers (
        org_id,
        uuid,
        first_name,
        last_name,
        position,
        session_duration,
        degree
    )
SELECT o.org_id,
    '',
    'Имя' || j,
    'Фамилия' || j,
    CASE
        (o.org_id % 3)
        WHEN 0 THEN 'Терапевт'
        WHEN 1 THEN 'Тренер'
        ELSE 'Библиотекарь'
    END,
    30 + (random() * 90)::int,
    'Степень сотрудника'
FROM orgs o,
    generate_series(1, 5) AS j;
-- Привязываем сотрудников к услугам случайно
INSERT INTO worker_services (worker_id, service_id)
SELECT w.worker_id,
    s.service_id
FROM workers w
    JOIN services s ON w.org_id = s.org_id
ORDER BY random()
LIMIT 30;
-- Создаем расписания сотрудников на каждый день недели
INSERT INTO worker_schedules (org_id, worker_id, weekday, start, over)
SELECT w.org_id,
    w.worker_id,
    weekday,
    '2024-11-28 08:00:00',
    '2024-11-28 18:00:00'
FROM workers w,
    generate_series(1, 7) AS weekday;
-- Создаем слоты на текущую неделю
INSERT INTO slots (
        worker_schedule_id,
        worker_id,
        date,
        session_begin,
        session_end,
        busy
    )
SELECT ws.worker_schedule_id,
    ws.worker_id,
    CURRENT_DATE + (
        ws.weekday - EXTRACT(
            DOW
            FROM CURRENT_DATE
        )
    )::int AS date,
    CURRENT_DATE + (
        ws.weekday - EXTRACT(
            DOW
            FROM CURRENT_DATE
        )
    )::int + TIME '09:00' + ((i -1) * INTERVAL '1 hour') AS session_begin,
    CURRENT_DATE + (
        ws.weekday - EXTRACT(
            DOW
            FROM CURRENT_DATE
        )
    )::int + TIME '10:00' + ((i -1) * INTERVAL '1 hour') AS session_end,
    (random() > 0.5)
FROM worker_schedules ws,
    generate_series(1, 5) AS i;
-- Генерируем случайные записи клиентов
INSERT INTO records (
        reviewed,
        slot_id,
        service_id,
        worker_id,
        user_id,
        org_id,
        is_canceled,
        cancel_reason
    )
SELECT DISTINCT ON (s.slot_id) (random() > 0.4),
    s.slot_id,
    ws.service_id,
    s.worker_id,
    (
        SELECT user_id
        FROM users
        ORDER BY random()
        LIMIT 1
    ), w.org_id, (random() > 0.8), CASE
        WHEN random() > 0.7 THEN 'Проблемы со здоровьем'
        WHEN random() > 0.4 THEN 'Планы изменились'
        ELSE ''
    END
FROM slots s
    JOIN workers w ON w.worker_id = s.worker_id
    JOIN worker_services ws ON ws.worker_id = s.worker_id
WHERE s.busy = TRUE
ORDER BY s.slot_id,
    random();
-- Генерируем отзывы к части записей
INSERT INTO feedbacks (record_id, stars, feedback)
SELECT r.record_id,
    (1 + random() * 4)::int,
    'Отзыв клиента'
FROM records r
WHERE r.reviewed = TRUE;