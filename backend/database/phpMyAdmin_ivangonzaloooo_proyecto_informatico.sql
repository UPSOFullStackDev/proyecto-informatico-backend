-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: mysql-ivangonzaloooo.alwaysdata.net
-- Generation Time: Oct 16, 2023 at 10:35 PM
-- Server version: 10.6.14-MariaDB
-- PHP Version: 7.4.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ivangonzaloooo_proyecto_informatico`
--

CREATE DATABASE IF NOT EXISTS `ivangonzaloooo_proyecto_informatico` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `ivangonzaloooo_proyecto_informatico`;

-- --------------------------------------------------------

--
-- Table structure for table `Bill`
--

CREATE TABLE `Bill` (
  `idBill` int(11) NOT NULL,
  `Client_idClient` int(11) NOT NULL,
  `price` int(11) DEFAULT NULL,
  `date` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `BillDetail`
--

CREATE TABLE `BillDetail` (
  `Bill_idBill` int(11) NOT NULL,
  `Product_idProduct` int(11) NOT NULL,
  `Service_idService` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Client`
--

CREATE TABLE `Client` (
  `idClient` int(11) NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  `surname` varchar(45) DEFAULT NULL,
  `address` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `password` varchar(45) DEFAULT NULL,
  `User_idUser` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Product`
--

CREATE TABLE `Product` (
  `idProduct` int(11) NOT NULL,
  `name` varchar(45) NOT NULL,
  `stock` int(11) NOT NULL,
  `description` varchar(45) DEFAULT NULL,
  `price` int(11) NOT NULL,
  `User_idUser` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Service`
--

CREATE TABLE `Service` (
  `idService` int(11) NOT NULL,
  `price` int(11) NOT NULL,
  `name` varchar(45) NOT NULL,
  `description` varchar(45) DEFAULT NULL,
  `User_idUser` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `User`
--

CREATE TABLE `User` (
  `idUser` int(11) NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  `username` varchar(45) DEFAULT NULL,
  `password` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Bill`
--
ALTER TABLE `Bill`
  ADD PRIMARY KEY (`idBill`,`Client_idClient`),
  ADD KEY `fk_Bill_Client1_idx` (`Client_idClient`);

--
-- Indexes for table `BillDetail`
--
ALTER TABLE `BillDetail`
  ADD PRIMARY KEY (`Bill_idBill`,`Product_idProduct`,`Service_idService`),
  ADD KEY `fk_Bill_has_Product_Product1_idx` (`Product_idProduct`),
  ADD KEY `fk_Bill_has_Product_Bill_idx` (`Bill_idBill`),
  ADD KEY `fk_BillDetail_Service1_idx` (`Service_idService`);

--
-- Indexes for table `Client`
--
ALTER TABLE `Client`
  ADD PRIMARY KEY (`idClient`,`User_idUser`),
  ADD KEY `fk_Client_User1_idx` (`User_idUser`);

--
-- Indexes for table `Product`
--
ALTER TABLE `Product`
  ADD PRIMARY KEY (`idProduct`,`User_idUser`),
  ADD KEY `fk_Product_User1_idx` (`User_idUser`);

--
-- Indexes for table `Service`
--
ALTER TABLE `Service`
  ADD PRIMARY KEY (`idService`,`User_idUser`),
  ADD KEY `fk_Service_User1_idx` (`User_idUser`);

--
-- Indexes for table `User`
--
ALTER TABLE `User`
  ADD PRIMARY KEY (`idUser`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Bill`
--
ALTER TABLE `Bill`
  ADD CONSTRAINT `fk_Bill_Client1` FOREIGN KEY (`Client_idClient`) REFERENCES `Client` (`idClient`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `BillDetail`
--
ALTER TABLE `BillDetail`
  ADD CONSTRAINT `fk_BillDetail_Service1` FOREIGN KEY (`Service_idService`) REFERENCES `Service` (`idService`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_Bill_has_Product_Bill` FOREIGN KEY (`Bill_idBill`) REFERENCES `Bill` (`idBill`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_Bill_has_Product_Product1` FOREIGN KEY (`Product_idProduct`) REFERENCES `Product` (`idProduct`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `Client`
--
ALTER TABLE `Client`
  ADD CONSTRAINT `fk_Client_User1` FOREIGN KEY (`User_idUser`) REFERENCES `User` (`idUser`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `Product`
--
ALTER TABLE `Product`
  ADD CONSTRAINT `fk_Product_User1` FOREIGN KEY (`User_idUser`) REFERENCES `User` (`idUser`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `Service`
--
ALTER TABLE `Service`
  ADD CONSTRAINT `fk_Service_User1` FOREIGN KEY (`User_idUser`) REFERENCES `User` (`idUser`) ON DELETE NO ACTION ON UPDATE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
