-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le :  jeu. 31 déc. 2020 à 11:24
-- Version du serveur :  10.4.10-MariaDB
-- Version de PHP :  7.3.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données :  `nanami.demo`
--
CREATE DATABASE IF NOT EXISTS `nanami.demo` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `nanami.demo`;

-- --------------------------------------------------------

--
-- Structure de la table `faction`
--

DROP TABLE IF EXISTS `faction`;
CREATE TABLE IF NOT EXISTS `faction` (
  `ID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `Name` varchar(64) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `faction`
--

INSERT INTO `faction` (`ID`, `Name`) VALUES
(1, 'Humain'),
(2, 'Exécuteur'),
(3, 'Revenant');

-- --------------------------------------------------------

--
-- Structure de la table `fellows`
--

DROP TABLE IF EXISTS `fellows`;
CREATE TABLE IF NOT EXISTS `fellows` (
  `ID` int(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  `User_ID` bigint(20) UNSIGNED NOT NULL,
  `Name` varchar(64) CHARACTER SET utf8mb4 NOT NULL,
  `Gold` int(11) NOT NULL,
  `Faction` int(10) UNSIGNED NOT NULL DEFAULT 1,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `User_ID` (`User_ID`),
  KEY `Name` (`Name`),
  KEY `f_user_faction` (`Faction`)
) ENGINE=InnoDB AUTO_INCREMENT=1042 DEFAULT CHARSET=utf8;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `fellows`
--
ALTER TABLE `fellows`
  ADD CONSTRAINT `f_user_faction` FOREIGN KEY (`Faction`) REFERENCES `faction` (`ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
