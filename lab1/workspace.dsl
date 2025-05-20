workspace  {
    name "Conference site"
    !identifiers hierarchical
    
    model {
        user = Person "Пользователь"
        conference_organization = softwareSystem "Conference Organization System" {
            
            description "Веб-приложение для организации конференций"

            dbSql = container "База данных" {
                description "База данных для хранения информации о пользователях, докладах и конференциях"
                technology "PostgreSQL"
                tags "Database"
                
            }

            dbNoSql = container "База данных" {
                description "База данных для хранения информации о пользователях, докладах и конференциях"
                technology "PostgreSQL"
                tags "Database"
                
            }

            user_control = container "Система контроля пользователей" {
                description "Регистрация и управление всеми пользователями"
                technology "FastApi"
                component "Conference User"
                component "Login"
                -> dbSql "Создание нового пользователя или поиск существующего"
            }

            lecture_control = container "Система контроля докладов" {
                description "Создание и управление всеми докладами"
                technology "FastApi"
                component "Lecture"
                -> dbNoSql "Создание нового доклада/поиск существующего"
            }

            conference_control = container "Система контроля конференций" {
                description "Создание и управление всеми конференциями"
                technology "FastApi"
                component "Conference"
                -> dbNoSql "Создание новой конференции/поиск существующей"
            }

            web_interface = container "Веб-интерфейс" {
                description "Пользовательский интерфейс для проведения конференции"
                technology "React"
                -> user_control "Отправка сообщения" "REST"
                -> lecture_control "Отправка сообщения" "REST"
                -> conference_control "Отправка сообщения" "REST"
            }
        }

        user -> conference_organization.web_interface "Взаимодействие с конференцией через платформу"
    }

    views {
        themes default
        
        systemContext conference_organization {
            include *
            autoLayout
        }

        container conference_organization {
            include *
            autoLayout
        }

        component conference_organization.user_control "users_components" {
            include *
            autoLayout
        }

        component conference_organization.lecture_control "lecture_components" {
            include *
            autoLayout
        }

        component conference_organization.conference_control "conference_components" {
            include *
            autoLayout
        }

        dynamic conference_organization {
            title "Добавление доклада в конференцию"
            user -> conference_organization.web_interface "Создание доклада"
            conference_organization.web_interface -> conference_organization.lecture_control "POST /lecture"
            conference_organization.lecture_control -> conference_organization.dbNoSql "Сохранение доклада"
            conference_organization.lecture_control -> conference_organization.web_interface "Получение id доклада"
            conference_organization.web_interface -> conference_organization.conference_control "POST /conference/lecture"
            conference_organization.conference_control -> conference_organization.dbNoSql "Обновление конференции"
            autoLayout lr
        }
        
        dynamic conference_organization {
            title "Создание пользователя"
            user -> conference_organization.web_interface "Заполнение формы регистрации"
            conference_organization.web_interface -> conference_organization.user_control "POST /conference_user"
            conference_organization.user_control -> conference_organization.dbSql "Сохранение данных"
            autoLayout lr
        }
    }
}