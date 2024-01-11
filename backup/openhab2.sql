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
-- Table structure for table `alert_timers`
--

DROP TABLE IF EXISTS `alert_timers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alert_timers` (
  `id` int NOT NULL,
  `alert_name` varchar(30) NOT NULL,
  `timer_value` int NOT NULL,
  `timer_units` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alert_timers`
--

LOCK TABLES `alert_timers` WRITE;
/*!40000 ALTER TABLE `alert_timers` DISABLE KEYS */;
INSERT INTO `alert_timers` VALUES (0,'door_alarm',2,'minutes'),(1,'turn_off_devices_alarm',30,'seconds');
/*!40000 ALTER TABLE `alert_timers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `new_item_names`
--

DROP TABLE IF EXISTS `new_item_names`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `new_item_names` (
  `thing_id` int NOT NULL,
  `item_id` int NOT NULL,
  `new_item_name` varchar(500) NOT NULL,
  PRIMARY KEY (`thing_id`,`item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `new_item_names`
--

LOCK TABLES `new_item_names` WRITE;
/*!40000 ALTER TABLE `new_item_names` DISABLE KEYS */;
INSERT INTO `new_item_names` VALUES (1,1,'Humidity Sensor');
/*!40000 ALTER TABLE `new_item_names` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `room_status`
--

DROP TABLE IF EXISTS `room_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `room_status` (
  `id` int NOT NULL AUTO_INCREMENT,
  `status` tinyint(1) NOT NULL,
  `amount` int NOT NULL,
  `timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `room_status`
--

LOCK TABLES `room_status` WRITE;
/*!40000 ALTER TABLE `room_status` DISABLE KEYS */;
INSERT INTO `room_status` VALUES (1,0,0,'2023-11-27 16:16:00'),(2,0,0,'2023-11-28 21:44:50'),(3,1,2,'2023-12-10 17:23:13'),(4,0,0,'2023-12-10 17:23:36');
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
  `thing_name` varchar(500) NOT NULL,
  `item_type` varchar(500) NOT NULL,
  `item_name` varchar(500) NOT NULL,
  `measurement_name` varchar(500) NOT NULL,
  `auto_switchoff` tinyint(1) NOT NULL,
  PRIMARY KEY (`thing_id`,`item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `thing_item_measurement`
--

LOCK TABLES `thing_item_measurement` WRITE;
/*!40000 ALTER TABLE `thing_item_measurement` DISABLE KEYS */;
INSERT INTO `thing_item_measurement` VALUES (1,1,'01 Humidity Sensor','Number:Dimensionless','Humidity_Sensor_Humidity_01_01','Humidity',0),(2,1,'02 Pressure Sensor','Number:Pressure','Pressure_Sensor_Pressure_02_01','Pressure',0),(3,1,'03 Temperature Sensor','Number:Temperature','Temperature_Sensor_Temperature_03_01','Temperature',0),(6,1,'06 WaterLeak Sensor','Switch','WaterLeak_Sensor_waterleakage_06_01','waterleakage',0),(7,1,'07 GAS Sensor switch','Switch','Smart_Metering_switchbinary_07_01','binary',0),(7,2,'07 GAS Sensor','Number','Smart_Metering_meterwatts_07_02','meterwatts',0),(8,1,'08 TV1','Switch','Smart_Metering_switchbinary_08_01','switchbinary',1),(8,2,'08 TV1','Number','Smart_Metering_meterwatts_08_02','meterwatts',0),(9,1,'09 TV2','Switch','Smart_Metering_switchbinary_09_01','switchbinary',1),(9,2,'09 TV2','Number','Smart_Metering_meterwatts_09_02','meterwatts',0),(10,1,'10 Living Lamps','Switch','Smart_Metering_switchbinary_10_01','switchbinary',1),(10,2,'10 Living Lamps','Number','Smart_Metering_meterwatts_10_02','meterwatts',0),(11,1,'11 Window Sensor','Contact','Window_Sensor_sensordoor_11_01','sensordoor',0),(12,1,'12 Door Sensor','Contact','Door_Sensor_sensordoor_12_01','sensordoor',0),(13,1,'13 Motion Sensor','Number:Temperature','Motion_Sensor_temperature_13_01','temperature',0),(13,2,'13 Motion Sensor','Number:Illuminance','Motion_Sensor_luminance_13_02','luminance',0),(13,3,'13 Motion Sensor','Switch','Motion_Sensor_alarmotion_13_03','alarmotion',0),(14,1,'14 Motion Sensor','Switch','Motion_Sensor_alarmotion_14_01','alarmotion',0),(15,1,'15 Motion Sensor','Switch','Motion_Sensor_alarmotion_15_01','alarmotion',0),(16,1,'16 Motion Sensor','Switch','Motion_Sensor_alarmotion_16_01','alarmotion',0),(17,1,'17 Motion Sensor','Switch','Motion_Sensor_alarmotion_17_01','alarmotion',0),(18,1,'18 Energy Meter','Number','Energy_Meter_metervoltage_18_01','metervoltage',0),(19,1,'19 Color LED Lamp','Switch','Color_LED_Lamp_switch_19_01','switch',0),(19,2,'19 Color LED Lamp','Dimmer','Color_LED_Lamp_brightness_19_01','brightness',0),(19,3,'19 Color LED Lamp','Color','Color_LED_Lamp_color_19_02','color',0),(21,1,'21 Ceiling Lamp','Switch','Ceiling_Lamp_switch_21_01','switch',0),(21,2,'21 Ceiling Lamp','Dimmer','Ceiling_Lamp_brightness_21_02','brightness',0),(21,3,'21 Ceiling Lamp','Color','Ceiling_Lamp_color_21_03','color',0),(22,1,'22 IP Camera','String','IP_Camera_Image_22_01','Image',0),(1000,1,'1000 Total Energy','Number','Total_Energy_Consumption_1000_01','Consumption',0),(1000,2,'1000 LED Lights','Switch','LED_Lights_switch_1000_02','switch',1),(1000,3,'1000 LED Lights','Dimmer','LED_Lights_brightness_1000_03','brightness',0),(1000,4,'1000 LED Lights','Color','LED_Lights_color_1000_04','color',0),(1000,5,'1000 Number people','String','Number_people_detection_1000_05','detection',0);
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
  `user_type` int NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  KEY `fk_user_type` (`user_type`),
  CONSTRAINT `fk_user_type` FOREIGN KEY (`user_type`) REFERENCES `user_types` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (3,'username','email@app.com','pbkdf2:sha256:260000$8XtrzNwJclKvnjMc$12002502ce75f3a20930db3c6caa4690a5499b6767817a863f68effaa6fba74b',0,'2021-12-09 23:26:01',NULL),(4,'dfa','dfa@gmail.com','pbkdf2:sha256:260000$vDkPj3AglCUGNBI0$f8f577aff70f41168600a7e6c89867d89372852dc66f2f4bf61852a57d5d853e',0,'2023-11-07 15:39:28',NULL),(6,'userdsd','dsd@gmail.com','pbkdf2:sha256:260000$NoGnYNnhmPI2gaUi$b1472bc6aa2cf110234f3566bcc5150bcde50246b1480b55d5ac6257824da58c',1,'2023-11-11 15:00:08',NULL),(7,'userdsd1','dsd1@gmail.com','pbkdf2:sha256:260000$TvfiW51RjFR3ATOE$d7350de45050a9ff5b89949f6deef89da7aedd893adabbc900723650af41bdc9',1,'2023-12-20 20:29:51',NULL);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_types`
--

DROP TABLE IF EXISTS `user_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_types` (
  `id` int NOT NULL,
  `type` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_types`
--

LOCK TABLES `user_types` WRITE;
/*!40000 ALTER TABLE `user_types` DISABLE KEYS */;
INSERT INTO `user_types` VALUES (0,'user'),(1,'admin');
/*!40000 ALTER TABLE `user_types` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-01-11 13:14:44
