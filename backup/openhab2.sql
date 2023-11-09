-- MySQL dump 10.13  Distrib 8.0.35, for Linux (x86_64)
--
-- Host: localhost    Database: openhab2
-- ------------------------------------------------------
-- Server version	8.0.35-0ubuntu0.22.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `items`
--

DROP TABLE IF EXISTS `items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `items` (
  `ItemId` int NOT NULL AUTO_INCREMENT,
  `itemname` varchar(500) NOT NULL,
  PRIMARY KEY (`ItemId`)
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `items`
--

LOCK TABLES `items` WRITE;
/*!40000 ALTER TABLE `items` DISABLE KEYS */;
INSERT INTO `items` VALUES (1,'30_APARENT_EXPORT_KVAH'),(2,'30_APARENT_IMPORT_KVAH'),(3,'30_ACTIVE_IMPORT_KWH'),(4,'30_ACTIVE_EXPORT_KWH'),(5,'30_REACTIVE_IMPORT_KVARH'),(6,'30_REACTIVE_EXPORT_TRAFFI_KVARH'),(7,'07REACTIVEIMPORTKVARH_ValueasNumber'),(8,'07APARENTIMPORTKVAH_ValueasNumber'),(9,'07ACTIVEIMPORTKWH_ValueasNumber'),(10,'31_APPARENT_EXPORT_KVAH'),(11,'31REACTIVEIMPORTKVARH_ValueasNumber'),(12,'31_ACTIVE_IMPORT_KWH'),(13,'31_APPARENT_IMPORT_KVAH'),(14,'31_ACTIVE_EXPORT_KWH'),(15,'31_REACTIVE_EXPORT_TRAFFI_KVARH'),(16,'25_APARENT_IMPORT_KVAH'),(17,'25_REACTIVE_IMPORT_KVARH'),(18,'25_ACTIVE_IMPORT_KWH'),(19,'25_APARENT_EXPORT_KVAH'),(20,'25_ACTIVE_EXPORT_KWH'),(21,'13_REACTIVE_EXPORT_TRAFFI_KVARH'),(22,'13_ACTIVE_EXPORT_KWH'),(23,'13_REACTIVE_IMPORT_KVARH'),(24,'13_APARENT_IMPORT_KVAH'),(25,'13_ACTIVE_IMPORT_KWH'),(26,'04ACTIVEIMPORTKWH_ValueasNumber'),(27,'04APARENTIMPORTKVAH_ValueasNumber'),(28,'04REACTIVEIMPORTKVARH_ValueasNumber'),(29,'28VOLTAGEL1N_ValueasNumber'),(30,'28VOLTAGEL2N_ValueasNumber'),(31,'28ACTIVEPOWERL1_ValueasNumber'),(32,'28FREQUENCY_ValueasNumber'),(33,'28PHASEANGLEVOLTAGEL1_ValueasNumber'),(34,'28APARENTIMPORTKVAH_ValueasNumber'),(35,'28ACTIVEIMPORTKWH_ValueasNumber'),(36,'28REACTIVEIMPORTKVARH_ValueasNumber'),(37,'01REACTIVEIMPORTKVARH_ValueasNumber'),(38,'01APARENTIMPORTKVAH_ValueasNumber'),(39,'27REACTIVEIMPORTKVARH_ValueasNumber'),(40,'27_ACTIVE_EXPORT_KWH'),(41,'27_ACTIVE_IMPORT_KWH'),(42,'27_APARENT_IMPORT_KVAH'),(43,'27_APARENT_EXPORT_KVAH'),(44,'26_APPARENT_NET_KVAH'),(45,'26_APARENT_EXPORT_KVAH'),(46,'26_REACTIVE_EXPORT_TRARIFF1_KVARH'),(47,'26_APPARENT_IMPORT_KVAH'),(48,'26_ACTIVE_IMPORT_KWH'),(49,'26_ACTIVE_EXPORT_KWH'),(50,'28ACTIVENETL1_ValueasNumber'),(51,'10APARENTIMPORTKVAH_ValueasNumber'),(52,'10ACTIVEIMPORTKWH_ValueasNumber'),(53,'10REACTIVEIMPORTKVARH_ValueasNumber'),(54,'29_ACTIVE_IMPORT_KWH'),(55,'29_ACTIVE_EXPORT_KWH'),(56,'29_APPARENT_IMPORT_KVAH'),(57,'29_REACTIVE_EXPORT_TRAFFI_KVARH'),(58,'29_APPARENT_EXPORT_KVARH'),(59,'ZWaveNode006MotionSensor_BatteryLevel'),(60,'ZWaveNode006MotionSensor_Sensorseismicintensity'),(61,'ZWaveNode006Motionsensor_Sensortemperature'),(62,'ZWaveNode006MotionSensor_Sensorluminance'),(63,'ZWaveNode006MotionSensor_TamperAlarm'),(64,'ZWaveSerialController_ReceivedChecksumErrors'),(65,'ZWaveNode006MotionSensor_BinarySensor'),(66,'ZWaveSerialController_OOFBytesReceived'),(67,'ZWaveNode004HS2SKZSmartMeteringPlug_Electricmeterwatts'),(68,'ZWaveNode006MotionSensor_MotionAlarm'),(69,'ZWaveSerialController_FramesAcknowledged'),(70,'ZWaveNode006MotionSensor_Alarmgeneral'),(71,'ZWaveNode004HS2SKZSmartMeteringPlug_Switch'),(72,'ZWaveSerialController_StartFrames');
/*!40000 ALTER TABLE `items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `names`
--

DROP TABLE IF EXISTS `names`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `names` (
  `ID` varchar(2) NOT NULL,
  `NAME` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `names`
--

LOCK TABLES `names` WRITE;
/*!40000 ALTER TABLE `names` DISABLE KEYS */;
INSERT INTO `names` VALUES ('01',''),('04',''),('07',''),('10',''),('13','Oven'),('25','Washing Machine'),('26','Dish Washer'),('27',''),('28','Microwave'),('29','Oven Fan'),('30','Refrigerator'),('31','Dryer Machine');
/*!40000 ALTER TABLE `names` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `relations`
--

DROP TABLE IF EXISTS `relations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `relations` (
  `ID` varchar(2) NOT NULL,
  `ACTIVEIMPORTID` varchar(2) DEFAULT NULL,
  `ACTIVEEXPORTID` varchar(2) DEFAULT NULL,
  `REACTIVEIMPORTID` varchar(2) DEFAULT NULL,
  `REACTIVEEXPORTID` varchar(2) DEFAULT NULL,
  `APPARENTIMPORTID` varchar(2) DEFAULT NULL,
  `APPARENTEXPORTID` varchar(2) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `relations`
--

LOCK TABLES `relations` WRITE;
/*!40000 ALTER TABLE `relations` DISABLE KEYS */;
INSERT INTO `relations` VALUES ('01','','','37','','38',''),('04','26','','28','','27',''),('07','09','','07','','08',''),('10','52','','53','','51',''),('13','25','22','23','21','24',''),('25','18','20','17','','16','19'),('26','48','49','','46','47','45'),('27','41','40','39','','42','43'),('28','35','','36','','34',''),('29','54','55','','57','56','58'),('30','03','04','05','06','02','01'),('31','12','14','11','15','13','10');
/*!40000 ALTER TABLE `relations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(20) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password` text NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (3,'username','email@app.com','pbkdf2:sha256:260000$8XtrzNwJclKvnjMc$12002502ce75f3a20930db3c6caa4690a5499b6767817a863f68effaa6fba74b','2021-12-09 23:26:01',NULL);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-11-09  0:31:17
