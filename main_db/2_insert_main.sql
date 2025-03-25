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
VALUES (
        '',
        'ivan.ivanov@example.com',
        'hashed_password1',
        'Иван',
        'Иванов',
        '+73431234567',
        'Москва',
        'Люблю путешествовать и заниматься спортом.',
        true
    ),
    (
        '',
        'elena.petrova@example.com',
        'hashed_password2',
        'Елена',
        'Петрова',
        '+73431234568',
        'Санкт-Петербург',
        'Работаю в IT и увлекаюсь фотографией.',
        true
    ),
    (
        '',
        'sergey.sidorov@example.com',
        'hashed_password3',
        'Сергей',
        'Сидоров',
        '+73431234569',
        'Новосибирск',
        'Инженер-электронщик с 10-летним опытом.',
        true
    );
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
VALUES (
        '',
        'clinic.moscow@example.com',
        'hashed_password4',
        'Клиника здоровья',
        4.8,
        'pharmacy',
        'Москва',
        'ул. Ленина, д. 10',
        '+73431234570',
        55.7558,
        37.6173,
        'Оказываем услуги диагностики и лечения.',
        true
    ),
    (
        '',
        'gym.spb@example.com',
        'hashed_password5',
        'Фитнес-центр Спорт',
        4.6,
        'gym',
        'Санкт-Петербург',
        'пр. Невский, д. 20',
        '+73431234571',
        59.9343,
        30.3351,
        'Современное оборудование и профессиональные тренеры.',
        true
    ),
    (
        '',
        'library.nsk@example.com',
        'hashed_password6',
        'Библиотека знаний',
        4.9,
        'education',
        'Новосибирск',
        'ул. Красный проспект, д. 5',
        '+73431234572',
        55.0084,
        82.9357,
        'Крупнейшая библиотека региона с богатым фондом.',
        true
    );
INSERT INTO timetables (
        org_id,
        weekday,
        open,
        close,
        break_start,
        break_end
    )
VALUES (
        1,
        1,
        '2024-11-28 08:00:00',
        '2024-11-28 20:00:00',
        '2024-11-28 12:00:00',
        '2024-11-28 13:00:00'
    ),
    (
        1,
        2,
        '2024-11-28 08:00:00',
        '2024-11-28 20:00:00',
        '2024-11-28 12:00:00',
        '2024-11-28 13:00:00'
    ),
    (
        1,
        3,
        '2024-11-28 08:00:00',
        '2024-11-28 20:00:00',
        '2024-11-28 12:00:00',
        '2024-11-28 13:00:00'
    ),
    (
        1,
        4,
        '2024-11-28 08:00:00',
        '2024-11-28 20:00:00',
        '2024-11-28 12:00:00',
        '2024-11-28 13:00:00'
    ),
    (
        1,
        5,
        '2024-11-28 08:00:00',
        '2024-11-28 20:00:00',
        '2024-11-28 12:00:00',
        '2024-11-28 13:00:00'
    ),
    (
        2,
        1,
        '2024-11-28 06:00:00',
        '2024-11-28 22:00:00',
        '2024-11-28 14:00:00',
        '2024-11-28 15:00:00'
    ),
    (
        2,
        1,
        '2024-11-28 06:00:00',
        '2024-11-28 22:00:00',
        '2024-11-28 14:00:00',
        '2024-11-28 15:00:00'
    ),
    (
        2,
        2,
        '2024-11-28 06:00:00',
        '2024-11-28 22:00:00',
        '2024-11-28 14:00:00',
        '2024-11-28 15:00:00'
    ),
    (
        2,
        3,
        '2024-11-28 06:00:00',
        '2024-11-28 22:00:00',
        '2024-11-28 14:00:00',
        '2024-11-28 15:00:00'
    ),
    (
        2,
        4,
        '2024-11-28 06:00:00',
        '2024-11-28 22:00:00',
        '2024-11-28 14:00:00',
        '2024-11-28 15:00:00'
    ),
    (
        2,
        5,
        '2024-11-28 06:00:00',
        '2024-11-28 22:00:00',
        '2024-11-28 14:00:00',
        '2024-11-28 15:00:00'
    ),
    (
        3,
        1,
        '2024-11-28 10:00:00',
        '2024-11-28 18:00:00',
        '2024-11-28 13:00:00',
        '2024-11-28 14:00:00'
    ),
    (
        3,
        2,
        '2024-11-28 10:00:00',
        '2024-11-28 18:00:00',
        '2024-11-28 13:00:00',
        '2024-11-28 14:00:00'
    ),
    (
        3,
        3,
        '2024-11-28 10:00:00',
        '2024-11-28 18:00:00',
        '2024-11-28 13:00:00',
        '2024-11-28 14:00:00'
    ),
    (
        3,
        4,
        '2024-11-28 10:00:00',
        '2024-11-28 18:00:00',
        '2024-11-28 13:00:00',
        '2024-11-28 14:00:00'
    ),
    (
        3,
        5,
        '2024-11-28 10:00:00',
        '2024-11-28 18:00:00',
        '2024-11-28 13:00:00',
        '2024-11-28 14:00:00'
    ),
    (
        3,
        6,
        '2024-11-28 10:00:00',
        '2024-11-28 18:00:00',
        '2024-11-28 13:00:00',
        '2024-11-28 14:00:00'
    );
INSERT INTO services (org_id, name, cost, description)
VALUES (
        1,
        'Общий осмотр',
        1200.00,
        'Проведение общего осмотра терапевтом.'
    ),
    (
        2,
        'Персональная тренировка',
        1500.00,
        'Индивидуальные занятия с профессиональным тренером.'
    );
INSERT INTO workers (
        org_id,
        uuid,
        first_name,
        last_name,
        position,
        session_duration,
        degree
    )
VALUES (
        1,
        '',
        'Анна',
        'Кузнецова',
        'Терапевт',
        60,
        'Кандидат медицинских наук'
    ),
    (
        2,
        '',
        'Дмитрий',
        'Смирнов',
        'Тренер',
        60,
        'Мастер спорта международного класса'
    ),
    (
        3,
        '',
        'Мария',
        'Васильева',
        'Библиотекарь',
        60,
        'Доктор филологических наук'
    );
INSERT INTO worker_services (worker_id, service_id)
VALUES (1, 1),
    -- Анна Кузнецова предоставляет услугу "Общий осмотр"
    (2, 2);
-- Дмитрий Смирнов предоставляет услугу "Персональная тренировка"
INSERT INTO worker_schedules (org_id, worker_id, weekday, start, over)
VALUES (
        1,
        1,
        1,
        '2024-11-28 08:00:00',
        '2024-11-28 20:00:00'
    ),
    -- Анна Кузнецова (Терапевт) на понедельник
    (
        1,
        1,
        2,
        '2024-11-29 08:00:00',
        '2024-11-29 20:00:00'
    ),
    -- Анна Кузнецова (Терапевт) на вторник
    (
        2,
        2,
        1,
        '2024-11-28 06:00:00',
        '2024-11-28 22:00:00'
    ),
    -- Дмитрий Смирнов (Тренер) на понедельник
    (
        2,
        2,
        2,
        '2024-11-29 06:00:00',
        '2024-11-29 22:00:00'
    ),
    -- Дмитрий Смирнов (Тренер) на вторник
    (
        3,
        3,
        1,
        '2024-11-28 10:00:00',
        '2024-11-28 18:00:00'
    ),
    -- Мария Васильева (Библиотекарь) на понедельник
    (
        3,
        3,
        2,
        '2024-11-29 10:00:00',
        '2024-11-29 18:00:00'
    );
-- Мария Васильева (Библиотекарь) на вторник
INSERT INTO slots (
        worker_schedule_id,
        worker_id,
        date,
        session_begin,
        session_end,
        busy
    )
VALUES (
        1,
        1,
        CURRENT_DATE,
        CURRENT_DATE + TIME '08:00:00',
        CURRENT_DATE + TIME '09:00:00',
        true
    ),
    (
        1,
        1,
        CURRENT_DATE,
        CURRENT_TIMESTAMP - INTERVAL '3 hour',
        CURRENT_TIMESTAMP - INTERVAL '1 hour',
        true
    ),
    (
        1,
        1,
        CURRENT_DATE + INTERVAL '1 day',
        CURRENT_DATE + INTERVAL '1 day' + TIME '08:00:00',
        CURRENT_DATE + TIME '09:00:00',
        true
    ),
    (
        1,
        1,
        CURRENT_DATE - INTERVAL '1 DAY',
        CURRENT_DATE + TIME '19:00:00',
        CURRENT_DATE + TIME '15:00:00',
        false
    ),
    (
        1,
        1,
        CURRENT_DATE,
        CURRENT_DATE + TIME '10:00:00',
        CURRENT_DATE + TIME '11:00:00',
        false
    ),
    (
        1,
        1,
        CURRENT_DATE,
        CURRENT_DATE + TIME '11:00:00',
        CURRENT_DATE + TIME '12:00:00',
        false
    ),
    (
        1,
        1,
        CURRENT_DATE,
        CURRENT_DATE + TIME '13:00:00',
        CURRENT_DATE + TIME '14:00:00',
        false
    ),
    (
        1,
        1,
        CURRENT_DATE,
        CURRENT_DATE + TIME '14:00:00',
        CURRENT_DATE + TIME '15:00:00',
        false
    ),
    (
        1,
        1,
        CURRENT_DATE,
        CURRENT_DATE + TIME '15:00:00',
        CURRENT_DATE + TIME '16:00:00',
        false
    ),
    (
        1,
        1,
        CURRENT_DATE,
        CURRENT_DATE + TIME '16:00:00',
        CURRENT_DATE + TIME '17:00:00',
        false
    ),
    (
        1,
        1,
        CURRENT_DATE,
        CURRENT_DATE + TIME '17:00:00',
        CURRENT_DATE + TIME '18:00:00',
        false
    ),
    (
        1,
        1,
        CURRENT_DATE,
        CURRENT_DATE + TIME '18:00:00',
        CURRENT_DATE + TIME '19:00:00',
        false
    ),
    (
        1,
        1,
        CURRENT_DATE,
        CURRENT_DATE + TIME '19:00:00',
        CURRENT_DATE + TIME '20:00:00',
        false
    ),
    (
        1,
        1,
        CURRENT_DATE + INTERVAL '1 DAY',
        CURRENT_DATE + INTERVAL '1 DAY' + TIME '19:00:00',
        CURRENT_DATE + INTERVAL '1 DAY' + TIME '15:00:00',
        false
    ),
    (
        2,
        2,
        CURRENT_DATE,
        CURRENT_DATE + TIME '06:00:00',
        CURRENT_DATE + TIME '07:00:00',
        false
    ),
    (
        2,
        2,
        CURRENT_DATE,
        CURRENT_DATE + TIME '07:00:00',
        CURRENT_DATE + TIME '08:00:00',
        false
    ),
    (
        2,
        2,
        CURRENT_DATE,
        CURRENT_DATE + TIME '08:00:00',
        CURRENT_DATE + TIME '09:00:00',
        false
    ),
    (
        2,
        2,
        CURRENT_DATE,
        CURRENT_DATE + TIME '09:00:00',
        CURRENT_DATE + TIME '10:00:00',
        false
    ),
    (
        2,
        2,
        CURRENT_DATE,
        CURRENT_DATE + TIME '10:00:00',
        CURRENT_DATE + TIME '11:00:00',
        false
    ),
    (
        2,
        2,
        CURRENT_DATE,
        CURRENT_DATE + TIME '11:00:00',
        CURRENT_DATE + TIME '12:00:00',
        false
    ),
    (
        2,
        2,
        CURRENT_DATE,
        CURRENT_DATE + TIME '12:00:00',
        CURRENT_DATE + TIME '13:00:00',
        false
    ),
    (
        2,
        2,
        CURRENT_DATE,
        CURRENT_DATE + TIME '13:00:00',
        CURRENT_DATE + TIME '14:00:00',
        false
    ),
    (
        2,
        2,
        CURRENT_DATE,
        CURRENT_DATE + TIME '14:00:00',
        CURRENT_DATE + TIME '15:00:00',
        false
    ),
    (
        2,
        2,
        CURRENT_DATE + INTERVAL '1 DAY',
        CURRENT_DATE + INTERVAL '1 DAY' + TIME '19:00:00',
        CURRENT_DATE + INTERVAL '1 DAY' + TIME '15:00:00',
        false
    ),
    (
        2,
        2,
        CURRENT_DATE - INTERVAL '1 DAY',
        CURRENT_DATE - INTERVAL '1 DAY' + TIME '19:00:00',
        CURRENT_DATE - INTERVAL '1 DAY' + TIME '15:00:00',
        false
    ),
    (
        3,
        3,
        CURRENT_DATE,
        CURRENT_DATE + TIME '10:00:00',
        CURRENT_DATE + TIME '11:00:00',
        false
    ),
    (
        3,
        3,
        CURRENT_DATE,
        CURRENT_DATE + TIME '11:00:00',
        CURRENT_DATE + TIME '12:00:00',
        false
    ),
    (
        3,
        3,
        CURRENT_DATE,
        CURRENT_DATE + TIME '12:00:00',
        CURRENT_DATE + TIME '13:00:00',
        false
    ),
    (
        3,
        3,
        CURRENT_DATE,
        CURRENT_DATE + TIME '13:00:00',
        CURRENT_DATE + TIME '14:00:00',
        false
    ),
    (
        3,
        3,
        CURRENT_DATE,
        CURRENT_DATE + TIME '14:00:00',
        CURRENT_DATE + TIME '15:00:00',
        false
    ),
    (
        3,
        3,
        CURRENT_DATE,
        CURRENT_DATE + TIME '15:00:00',
        CURRENT_DATE + TIME '16:00:00',
        false
    ),
    (
        3,
        3,
        CURRENT_DATE,
        CURRENT_DATE + TIME '16:00:00',
        CURRENT_DATE + TIME '17:00:00',
        false
    ),
    (
        3,
        3,
        CURRENT_DATE,
        CURRENT_DATE + TIME '17:00:00',
        CURRENT_DATE + TIME '18:00:00',
        false
    ),
    (
        3,
        3,
        CURRENT_DATE + INTERVAL '1 DAY',
        CURRENT_DATE + TIME '19:00:00',
        CURRENT_DATE + TIME '15:00:00',
        false
    ),
    (
        3,
        3,
        CURRENT_DATE - INTERVAL '1 DAY',
        CURRENT_DATE - INTERVAL '1 DAY' + TIME '19:00:00',
        CURRENT_DATE - INTERVAL '1 DAY' + TIME '15:00:00',
        false
    );
INSERT INTO records (
        reviewed,
        slot_id,
        service_id,
        worker_id,
        user_id,
        org_id
    )
VALUES (true, 1, 1, 1, 1, 1),
    (false, 2, 2, 2, 1, 2);
INSERT INTO feedbacks (record_id, stars, feedback)
VALUES (1, 5, 'Отличный сервис, очень доволен!');