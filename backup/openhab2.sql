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
-- Table structure for table `room_status`
--

DROP TABLE IF EXISTS `room_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `room_status` (
  `id` int NOT NULL AUTO_INCREMENT,
  `status` varchar(9) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '',
  `timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `room_status`
--

LOCK TABLES `room_status` WRITE;
/*!40000 ALTER TABLE `room_status` DISABLE KEYS */;
INSERT INTO `room_status` VALUES (1,'EMPTY','2023-11-24 11:16:37'),(2,'NOT EMPTY','2023-11-24 11:17:40'),(3,'EMPTY','2023-11-25 19:40:43'),(4,'EMPTY','2023-11-25 14:45:36'),(5,'EMPTY','2023-11-25 14:45:36'),(6,'EMPTY','2023-11-25 14:45:36'),(7,'EMPTY','2023-11-25 19:48:38'),(8,'EMPTY','2023-11-25 19:48:43'),(9,'EMPTY','2023-11-25 19:48:46'),(10,'EMPTY','2023-11-25 19:49:01'),(11,'EMPTY','2023-11-25 19:56:06');
/*!40000 ALTER TABLE `room_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `thing_item_measurement`
--

DROP TABLE IF EXISTS `thing_item_measurement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `thing_item_measurement` (
  `thing_id` int NOT NULL,
  `item_id` int NOT NULL,
  `thing_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `item_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `measurement_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`thing_id`,`item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `thing_item_measurement`
--

LOCK TABLES `thing_item_measurement` WRITE;
/*!40000 ALTER TABLE `thing_item_measurement` DISABLE KEYS */;
INSERT INTO `thing_item_measurement` VALUES (1,1,'01 Humidity Sensor','Humidity_Sensor_Humidity_01_01','Humidity'),(2,1,'02 Pressure Sensor','Pressure_Sensor_Pressure_02_01','Pressure'),(3,1,'03 Temperature Sensor','Temperature_Sensor_Temperature_03_01','Temperature'),(6,1,'06 WaterLeak Sensor','WaterLeak_Sensor_waterleakage_06_01','waterleakage'),(7,1,'07 GAS Sensor','Smart_Metering_switchbinary_07_01','switch binary'),(7,2,'07 GAS Sensor','Smart_Metering_meterwatts_07_02','meterwatts'),(8,1,'08 TV1','Smart_Metering_switchbinary_08_01','switchbinary'),(8,2,'08 TV1','Smart_Metering_meterwatts_08_02','meterwatts'),(9,1,'09 TV2','Smart_Metering_switchbinary_09_01','switchbinary'),(9,2,'09 TV2','Smart_Metering_meterwatts_09_02','meterwatts'),(10,1,'10 Living Lamps','Smart_Metering_switchbinary_10_01','switchbinary'),(10,2,'10 Living Lamps','Smart_Metering_meterwatts_10_02','meterwatts'),(11,1,'11 Window Sensor','Window_Sensor_sensordoor_11_01','sensordoor'),(12,1,'12 Door Sensor','Door_Sensor_sensordoor_12_01','sensordoor'),(13,1,'13 Motion Sensor','Motion_Sensor_temperature_13_01','temperature'),(13,2,'13 Motion Sensor','Motion_Sensor_luminance_13_02','luminance'),(13,3,'13 Motion Sensor','Motion_Sensor_alarmotion_13_03','alarmotion'),(14,1,'14 Motion Sensor','Motion_Sensor_alarmotion_14_01','alarmotion'),(15,1,'15 Motion Sensor','Motion_Sensor_alarmotion_15_01','alarmotion'),(16,1,'16 Motion Sensor','Motion_Sensor_alarmotion_16_01','alarmotion'),(17,1,'17 Motion Sensor','Motion_Sensor_alarmotion_17_01','alarmotion'),(18,1,'18 Energy Meter','Energy_Meter_metervoltage_18_01','metervoltage'),(19,1,'19 Color LED','Color_LED_Lamp_color_19_01','Lamp color'),(1000,1,'Total Energy Consumption','Total_Energy_Consumption_xx_01','Total Energy Consumption');
/*!40000 ALTER TABLE `thing_item_measurement` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (3,'username','email@app.com','pbkdf2:sha256:260000$8XtrzNwJclKvnjMc$12002502ce75f3a20930db3c6caa4690a5499b6767817a863f68effaa6fba74b','2021-12-09 23:26:01',NULL),(4,'dfa','dfa@gmail.com','pbkdf2:sha256:260000$vDkPj3AglCUGNBI0$f8f577aff70f41168600a7e6c89867d89372852dc66f2f4bf61852a57d5d853e','2023-11-07 15:39:28',NULL);
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

-- Dump completed on 2023-11-25 14:59:34
