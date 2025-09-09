CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    password VARCHAR(60) NOT NULL,
    role INT NOT NULL
);

INSERT INTO users(name, password, role) values
('HaduhManggAngelIki', "$2b$12$DWFsJOOlYW5ACZz4Y5w64.VPF/RP.ZNEYKFL3eWI/LfR/UL34SHzC", 1),
('MlakuMlakuNangTunjungan', "$2b$12$BWQ6szEY7tW2CIoYvpTMNOiAC4Prtbszg6kE3zComSDTfP7y6dShi", 0);