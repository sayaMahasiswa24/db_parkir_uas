-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 27, 2026 at 09:50 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `parkir`
--

-- --------------------------------------------------------

--
-- Table structure for table `parkir`
--

CREATE TABLE `parkir` (
  `id` int(11) NOT NULL,
  `plat_nomor` varchar(15) NOT NULL,
  `jenis_kendaraan` enum('Motor','Mobil') NOT NULL,
  `waktu_masuk` datetime DEFAULT current_timestamp(),
  `waktu_keluar` datetime DEFAULT NULL,
  `tarif` int(11) DEFAULT 0,
  `status` enum('Parkir','Selesai') DEFAULT 'Parkir'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `parkir`
--

INSERT INTO `parkir` (`id`, `plat_nomor`, `jenis_kendaraan`, `waktu_masuk`, `waktu_keluar`, `tarif`, `status`) VALUES
(1, 'B 1234 ABC', 'Mobil', '2026-01-28 02:46:15', NULL, 0, 'Parkir'),
(2, 'AB 5678 DE', 'Motor', '2026-01-28 02:46:15', NULL, 0, 'Parkir'),
(3, 'AC321', 'Motor', '2026-01-28 03:38:04', NULL, 0, 'Parkir'),
(4, 'AD 145', 'Motor', '2026-01-28 03:39:33', '2026-01-28 03:45:45', 2000, 'Selesai');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `parkir`
--
ALTER TABLE `parkir`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `parkir`
--
ALTER TABLE `parkir`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
