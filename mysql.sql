CREATE SCHEMA `hlook` DEFAULT CHARACTER SET utf8 ;

CREATE TABLE `hlook`.`information` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45),
  `address` TEXT,
  `city` VARCHAR(45),
  `country` VARCHAR(45),
  `countryCode` VARCHAR(4),
  `rating` INT,
  `longitude` DOUBLE,
  `latitude` DOUBLE,
  `description` TEXT,
  PRIMARY KEY (`id`));

CREATE TABLE `hlook`.`photos` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `master_id` INT NOT NULL,
  `link` TEXT,
  PRIMARY KEY (`id`),
  INDEX `InformationId_PhotosMasterId` (`master_id` ASC),
  CONSTRAINT `InformationIdPhotosMasterId`
    FOREIGN KEY (`master_id`)
    REFERENCES `hlook`.`information` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);