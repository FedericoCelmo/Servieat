-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema servieating
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema servieating
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `servieating` DEFAULT CHARACTER SET utf8 ;
USE `servieating` ;

-- -----------------------------------------------------
-- Table `servieating`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `servieating`.`user` (
  `iduser` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `correo` VARCHAR(100) NULL,
  `password` VARCHAR(100) NULL,
  `tipo` VARCHAR(45) NULL,
  `estatus` VARCHAR(45) NULL,
  `fecharegistro` DATETIME NULL,
  `ultimavez` DATETIME NULL,
  PRIMARY KEY (`iduser`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `servieating`.`comensal`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `servieating`.`comensal` (
  `idcomensal` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(100) NULL,
  `apellidoP` VARCHAR(45) NULL,
  `apellidoM` VARCHAR(45) NULL,
  `fotourl` VARCHAR(200) NULL,
  `user_iduser` INT NOT NULL,
  `calle` VARCHAR(45) NULL,
  `numero` VARCHAR(45) NULL,
  `cruzamiento1` VARCHAR(45) NULL,
  `cruzamiento2` VARCHAR(45) NULL,
  `colonia` VARCHAR(45) NULL,
  `cp` VARCHAR(45) NULL,
  `telefono` VARCHAR(45) NULL,
  `referencia` VARCHAR(100) NULL,
  `estatus` VARCHAR(45) NULL,
  PRIMARY KEY (`idcomensal`, `user_iduser`),
  INDEX `fk_comensal_user_idx` (`user_iduser` ASC) VISIBLE,
  CONSTRAINT `fk_comensal_user`
    FOREIGN KEY (`user_iduser`)
    REFERENCES `servieating`.`user` (`iduser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `servieating`.`restaurantero`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `servieating`.`restaurantero` (
  `idrestaurantero` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(100) NULL,
  `fotourl` VARCHAR(200) NULL,
  `user_iduser` INT NOT NULL,
  `descripcion` VARCHAR(300) NULL,
  `calle` VARCHAR(45) NULL,
  `numero` VARCHAR(45) NULL,
  `cruzamiento1` VARCHAR(45) NULL,
  `cruzamiento2` VARCHAR(45) NULL,
  `colonia` VARCHAR(45) NULL,
  `cp` VARCHAR(45) NULL,
  `telefono` VARCHAR(45) NULL,
  `url` VARCHAR(100) NULL,
  `referencia` VARCHAR(100) NULL,
  `tipo` VARCHAR(45) NULL,
  `horarioinicial` DATETIME NULL,
  `horariocierre` DATETIME NULL,
  `diaslaborales` VARCHAR(45) NULL,
  `diadescanso` VARCHAR(45) NULL,
  `whatsapp` VARCHAR(45) NULL,
  `eslogan` VARCHAR(100) NULL,
  `facebook` VARCHAR(50) NULL,
  PRIMARY KEY (`idrestaurantero`, `user_iduser`),
  INDEX `fk_restaurantero_user1_idx` (`user_iduser` ASC) VISIBLE,
  CONSTRAINT `fk_restaurantero_user1`
    FOREIGN KEY (`user_iduser`)
    REFERENCES `servieating`.`user` (`iduser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `servieating`.`menu`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `servieating`.`menu` (
  `idmenu` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  `descripcion` VARCHAR(200) NULL,
  `precio` VARCHAR(45) NULL,
  `estatus` VARCHAR(45) NULL,
  `restaurantero_idrestaurantero` INT NOT NULL,
  `restaurantero_user_iduser` INT NOT NULL,
  `fotourl` VARCHAR(200) NULL,
  `tipo` VARCHAR(45) NULL,
  `presentacion` VARCHAR(45) NULL,
  PRIMARY KEY (`idmenu`, `restaurantero_idrestaurantero`, `restaurantero_user_iduser`),
  INDEX `fk_menu_restaurantero1_idx` (`restaurantero_idrestaurantero` ASC, `restaurantero_user_iduser` ASC) VISIBLE,
  CONSTRAINT `fk_menu_restaurantero1`
    FOREIGN KEY (`restaurantero_idrestaurantero` , `restaurantero_user_iduser`)
    REFERENCES `servieating`.`restaurantero` (`idrestaurantero` , `user_iduser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `servieating`.`pedido`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `servieating`.`pedido` (
  `idpedido` INT NOT NULL AUTO_INCREMENT,
  `cantidad` VARCHAR(45) NULL,
  `total` VARCHAR(45) NULL,
  `menu_idmenu` INT NOT NULL,
  `menu_restaurantero_idrestaurantero` INT NOT NULL,
  `menu_restaurantero_user_iduser` INT NOT NULL,
  `comensal_idcomensal` INT NOT NULL,
  `comensal_user_iduser` INT NOT NULL,
  `horaregistro` DATETIME NULL,
  `tiempoentrega` VARCHAR(45) NULL,
  `estatus` VARCHAR(45) NULL,
  `modalidad` VARCHAR(45) NULL,
  `comentario` VARCHAR(100) NULL,
  PRIMARY KEY (`idpedido`, `menu_idmenu`, `menu_restaurantero_idrestaurantero`, `menu_restaurantero_user_iduser`, `comensal_idcomensal`, `comensal_user_iduser`),
  INDEX `fk_pedido_menu1_idx` (`menu_idmenu` ASC, `menu_restaurantero_idrestaurantero` ASC, `menu_restaurantero_user_iduser` ASC) VISIBLE,
  INDEX `fk_pedido_comensal1_idx` (`comensal_idcomensal` ASC, `comensal_user_iduser` ASC) VISIBLE,
  CONSTRAINT `fk_pedido_menu1`
    FOREIGN KEY (`menu_idmenu` , `menu_restaurantero_idrestaurantero` , `menu_restaurantero_user_iduser`)
    REFERENCES `servieating`.`menu` (`idmenu` , `restaurantero_idrestaurantero` , `restaurantero_user_iduser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_pedido_comensal1`
    FOREIGN KEY (`comensal_idcomensal` , `comensal_user_iduser`)
    REFERENCES `servieating`.`comensal` (`idcomensal` , `user_iduser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `servieating`.`mensaje`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `servieating`.`mensaje` (
  `idmensaje` INT NOT NULL AUTO_INCREMENT,
  `asunto` VARCHAR(50) NULL,
  `mensaje` VARCHAR(250) NULL,
  `estado` VARCHAR(45) NULL,
  `user_iduser` INT NOT NULL,
  `fecha` DATETIME NULL,
  PRIMARY KEY (`idmensaje`, `user_iduser`),
  INDEX `fk_mensaje_user1_idx` (`user_iduser` ASC) VISIBLE,
  CONSTRAINT `fk_mensaje_user1`
    FOREIGN KEY (`user_iduser`)
    REFERENCES `servieating`.`user` (`iduser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `servieating`.`megustarest`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `servieating`.`megustarest` (
  `idmegustarest` INT NOT NULL AUTO_INCREMENT,
  `restaurantero_idrestaurantero` INT NOT NULL,
  `restaurantero_user_iduser` INT NOT NULL,
  `estatus` VARCHAR(45) NULL,
  `comensal_idcomensal` INT NOT NULL,
  `comensal_user_iduser` INT NOT NULL,
  PRIMARY KEY (`idmegustarest`, `restaurantero_idrestaurantero`, `restaurantero_user_iduser`, `comensal_idcomensal`, `comensal_user_iduser`),
  INDEX `fk_megustarest_restaurantero1_idx` (`restaurantero_idrestaurantero` ASC, `restaurantero_user_iduser` ASC) VISIBLE,
  INDEX `fk_megustarest_comensal1_idx` (`comensal_idcomensal` ASC, `comensal_user_iduser` ASC) VISIBLE,
  CONSTRAINT `fk_megustarest_restaurantero1`
    FOREIGN KEY (`restaurantero_idrestaurantero` , `restaurantero_user_iduser`)
    REFERENCES `servieating`.`restaurantero` (`idrestaurantero` , `user_iduser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_megustarest_comensal1`
    FOREIGN KEY (`comensal_idcomensal` , `comensal_user_iduser`)
    REFERENCES `servieating`.`comensal` (`idcomensal` , `user_iduser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `servieating`.`megustamenu`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `servieating`.`megustamenu` (
  `idmegustamenu` INT NOT NULL AUTO_INCREMENT,
  `menu_idmenu` INT NOT NULL,
  `menu_restaurantero_idrestaurantero` INT NOT NULL,
  `menu_restaurantero_user_iduser` INT NOT NULL,
  `estatus` VARCHAR(45) NULL,
  `comensal_idcomensal` INT NOT NULL,
  `comensal_user_iduser` INT NOT NULL,
  PRIMARY KEY (`idmegustamenu`, `menu_idmenu`, `menu_restaurantero_idrestaurantero`, `menu_restaurantero_user_iduser`, `comensal_idcomensal`, `comensal_user_iduser`),
  INDEX `fk_megustamenu_menu1_idx` (`menu_idmenu` ASC, `menu_restaurantero_idrestaurantero` ASC, `menu_restaurantero_user_iduser` ASC) VISIBLE,
  INDEX `fk_megustamenu_comensal1_idx` (`comensal_idcomensal` ASC, `comensal_user_iduser` ASC) VISIBLE,
  CONSTRAINT `fk_megustamenu_menu1`
    FOREIGN KEY (`menu_idmenu` , `menu_restaurantero_idrestaurantero` , `menu_restaurantero_user_iduser`)
    REFERENCES `servieating`.`menu` (`idmenu` , `restaurantero_idrestaurantero` , `restaurantero_user_iduser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_megustamenu_comensal1`
    FOREIGN KEY (`comensal_idcomensal` , `comensal_user_iduser`)
    REFERENCES `servieating`.`comensal` (`idcomensal` , `user_iduser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `servieating`.`comentariorest`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `servieating`.`comentariorest` (
  `idcomentariorest` INT NOT NULL AUTO_INCREMENT,
  `restaurantero_idrestaurantero` INT NOT NULL,
  `restaurantero_user_iduser` INT NOT NULL,
  `comentario` VARCHAR(200) NULL,
  `fecha` DATETIME NULL,
  `comensal_idcomensal` INT NOT NULL,
  `comensal_user_iduser` INT NOT NULL,
  PRIMARY KEY (`idcomentariorest`, `restaurantero_idrestaurantero`, `restaurantero_user_iduser`, `comensal_idcomensal`, `comensal_user_iduser`),
  INDEX `fk_comentariorest_restaurantero1_idx` (`restaurantero_idrestaurantero` ASC, `restaurantero_user_iduser` ASC) VISIBLE,
  INDEX `fk_comentariorest_comensal1_idx` (`comensal_idcomensal` ASC, `comensal_user_iduser` ASC) VISIBLE,
  CONSTRAINT `fk_comentariorest_restaurantero1`
    FOREIGN KEY (`restaurantero_idrestaurantero` , `restaurantero_user_iduser`)
    REFERENCES `servieating`.`restaurantero` (`idrestaurantero` , `user_iduser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_comentariorest_comensal1`
    FOREIGN KEY (`comensal_idcomensal` , `comensal_user_iduser`)
    REFERENCES `servieating`.`comensal` (`idcomensal` , `user_iduser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `servieating`.`comentariomenu`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `servieating`.`comentariomenu` (
  `idcomentariomenu` INT NOT NULL AUTO_INCREMENT,
  `menu_idmenu` INT NOT NULL,
  `menu_restaurantero_idrestaurantero` INT NOT NULL,
  `menu_restaurantero_user_iduser` INT NOT NULL,
  `comentario` VARCHAR(200) NULL,
  `fecha` DATETIME NULL,
  `comensal_idcomensal` INT NOT NULL,
  `comensal_user_iduser` INT NOT NULL,
  PRIMARY KEY (`idcomentariomenu`, `menu_idmenu`, `menu_restaurantero_idrestaurantero`, `menu_restaurantero_user_iduser`, `comensal_idcomensal`, `comensal_user_iduser`),
  INDEX `fk_comentariomenu_menu1_idx` (`menu_idmenu` ASC, `menu_restaurantero_idrestaurantero` ASC, `menu_restaurantero_user_iduser` ASC) VISIBLE,
  INDEX `fk_comentariomenu_comensal1_idx` (`comensal_idcomensal` ASC, `comensal_user_iduser` ASC) VISIBLE,
  CONSTRAINT `fk_comentariomenu_menu1`
    FOREIGN KEY (`menu_idmenu` , `menu_restaurantero_idrestaurantero` , `menu_restaurantero_user_iduser`)
    REFERENCES `servieating`.`menu` (`idmenu` , `restaurantero_idrestaurantero` , `restaurantero_user_iduser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_comentariomenu_comensal1`
    FOREIGN KEY (`comensal_idcomensal` , `comensal_user_iduser`)
    REFERENCES `servieating`.`comensal` (`idcomensal` , `user_iduser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `servieating`.`respuestarest`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `servieating`.`respuestarest` (
  `idrespuestarest` INT NOT NULL AUTO_INCREMENT,
  `comentario` VARCHAR(200) NULL,
  `fecha` DATETIME NULL,
  `restaurantero_idrestaurantero` INT NOT NULL,
  `restaurantero_user_iduser` INT NOT NULL,
  PRIMARY KEY (`idrespuestarest`, `restaurantero_idrestaurantero`, `restaurantero_user_iduser`),
  INDEX `fk_respuestarest_restaurantero1_idx` (`restaurantero_idrestaurantero` ASC, `restaurantero_user_iduser` ASC) VISIBLE,
  CONSTRAINT `fk_respuestarest_restaurantero1`
    FOREIGN KEY (`restaurantero_idrestaurantero` , `restaurantero_user_iduser`)
    REFERENCES `servieating`.`restaurantero` (`idrestaurantero` , `user_iduser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `servieating`.`respuestamenu`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `servieating`.`respuestamenu` (
  `idrespuestamenu` INT NOT NULL AUTO_INCREMENT,
  `comentario` VARCHAR(200) NULL,
  `fecha` DATETIME NULL,
  `menu_idmenu` INT NOT NULL,
  `menu_restaurantero_idrestaurantero` INT NOT NULL,
  `menu_restaurantero_user_iduser` INT NOT NULL,
  `restaurantero_idrestaurantero` INT NOT NULL,
  `restaurantero_user_iduser` INT NOT NULL,
  PRIMARY KEY (`idrespuestamenu`, `menu_idmenu`, `menu_restaurantero_idrestaurantero`, `menu_restaurantero_user_iduser`, `restaurantero_idrestaurantero`, `restaurantero_user_iduser`),
  INDEX `fk_respuestamenu_menu1_idx` (`menu_idmenu` ASC, `menu_restaurantero_idrestaurantero` ASC, `menu_restaurantero_user_iduser` ASC) VISIBLE,
  INDEX `fk_respuestamenu_restaurantero1_idx` (`restaurantero_idrestaurantero` ASC, `restaurantero_user_iduser` ASC) VISIBLE,
  CONSTRAINT `fk_respuestamenu_menu1`
    FOREIGN KEY (`menu_idmenu` , `menu_restaurantero_idrestaurantero` , `menu_restaurantero_user_iduser`)
    REFERENCES `servieating`.`menu` (`idmenu` , `restaurantero_idrestaurantero` , `restaurantero_user_iduser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_respuestamenu_restaurantero1`
    FOREIGN KEY (`restaurantero_idrestaurantero` , `restaurantero_user_iduser`)
    REFERENCES `servieating`.`restaurantero` (`idrestaurantero` , `user_iduser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
