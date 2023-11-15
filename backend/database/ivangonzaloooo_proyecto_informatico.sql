-- MySQL dump 10.13  Distrib 8.0.31, for Win64 (x86_64)
-- Host: localhost    Database: ivangonzaloooo_proyecto_informatico
-- ------------------------------------------------------
-- Server version	8.0.31

CREATE SCHEMA IF NOT EXISTS `ivangonzaloooo_proyecto_informatico` DEFAULT CHARACTER SET utf8;
USE `ivangonzaloooo_proyecto_informatico`;

-- -----------------------------------------------------
-- Table `User`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `User`;

CREATE TABLE IF NOT EXISTS `User`(
  `idUser` INT NOT NULL,
  `name` VARCHAR(45) NULL,
  `username` VARCHAR(45) NULL,
  `password` VARCHAR(45) NULL,
  `email` VARCHAR(45) NULL,
  PRIMARY KEY (`idUser`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `Product`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Product`;

CREATE TABLE IF NOT EXISTS `Product` (
  `idProduct` INT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `stock` INT NOT NULL,
  `description` VARCHAR(45) NULL,
  `price` INT NOT NULL,
  `User_idUser` INT NOT NULL,
  PRIMARY KEY (`idProduct`, `User_idUser`),
  INDEX `fk_Product_User1_idx` (`User_idUser` ASC) VISIBLE,
  CONSTRAINT `fk_Product_User1`
    FOREIGN KEY (`User_idUser`)
    REFERENCES `User` (`idUser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `Client`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Client`;

CREATE TABLE IF NOT EXISTS `Client` (
  `idClient` INT NOT NULL,
  `name` VARCHAR(45) NULL,
  `surname` VARCHAR(45) NULL,
  `address` VARCHAR(45) NULL,
  `email` VARCHAR(45) NULL,
  `password` VARCHAR(45) NULL,
  `User_idUser` INT NOT NULL,
  PRIMARY KEY (`idClient`, `User_idUser`),
  INDEX `fk_Client_User1_idx` (`User_idUser` ASC) VISIBLE,
  CONSTRAINT `fk_Client_User1`
    FOREIGN KEY (`User_idUser`)
    REFERENCES `User` (`idUser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `Bill`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Bill`;

CREATE TABLE IF NOT EXISTS `Bill` (
  `idBill` INT NOT NULL,
  `Client_idClient` INT NOT NULL,
  `price` INT NULL,
  `date` DATETIME NULL,
  PRIMARY KEY (`idBill`, `Client_idClient`),
  INDEX `fk_Bill_Client1_idx` (`Client_idClient` ASC) VISIBLE,
  CONSTRAINT `fk_Bill_Client1`
    FOREIGN KEY (`Client_idClient`)
    REFERENCES `Client` (`idClient`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `Service`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Service`;

CREATE TABLE IF NOT EXISTS `Service` (
  `idService` INT NOT NULL,
  `price` INT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `description` VARCHAR(45) NULL,
  `User_idUser` INT NOT NULL,
  PRIMARY KEY (`idService`, `User_idUser`),
  INDEX `fk_Service_User1_idx` (`User_idUser` ASC) VISIBLE,
  CONSTRAINT `fk_Service_User1`
    FOREIGN KEY (`User_idUser`)
    REFERENCES `User` (`idUser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `BillDetail`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `BillDetail`;

CREATE TABLE IF NOT EXISTS `BillDetail` (
  `Bill_idBill` INT NOT NULL,
  `Product_idProduct` INT NULL,
  `Service_idService` INT NULL,
  PRIMARY KEY (`Bill_idBill`, `Product_idProduct`, `Service_idService`),
  INDEX `fk_Bill_has_Product_Product1_idx` (`Product_idProduct` ASC) VISIBLE,
  INDEX `fk_Bill_has_Product_Bill_idx` (`Bill_idBill` ASC) VISIBLE,
  INDEX `fk_BillDetail_Service1_idx` (`Service_idService` ASC) VISIBLE,
  CONSTRAINT `fk_Bill_has_Product_Bill`
    FOREIGN KEY (`Bill_idBill`)
    REFERENCES `Bill` (`idBill`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Bill_has_Product_Product1`
    FOREIGN KEY (`Product_idProduct`)
    REFERENCES `Product` (`idProduct`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_BillDetail_Service1`
    FOREIGN KEY (`Service_idService`)
    REFERENCES `Service` (`idService`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
