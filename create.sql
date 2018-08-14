create database gear_paper;
CREATE TABLE paper
(
    id int PRIMARY KEY NOT NULL AUTO_INCREMENT,
    title varchar(100),
    url varchar(200),
    year int,
    authors varchar(50),
    keywords varchar(50),
    abstract varchar(1000),
    publisher varchar(200),
    cite int,
    download int,
    unit varchar(100),
    reference varchar(200),
    category varchar(20)
);

CREATE TABLE `paper` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `url` varchar(200) CHARACTER SET utf8 DEFAULT NULL,
  `year` int(11) DEFAULT NULL,
  `authors` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `keywords` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `abstract` varchar(1000) CHARACTER SET utf8 DEFAULT NULL,
  `publisher` varchar(200) CHARACTER SET utf8 DEFAULT NULL,
  `cite` int(11) DEFAULT NULL,
  `download` int(11) DEFAULT NULL,
  `unit` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `reference` varchar(200) CHARACTER SET utf8 DEFAULT NULL,
  `category` varchar(20) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=In