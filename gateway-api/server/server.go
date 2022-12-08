package server

import (
	"fmt"
	"gateway-api/k8s"
	"github.com/gin-gonic/gin"
	"log"
	"net/http"
)

type addCameraRequest struct {
	CCTVId            int    `json:"cctvId"`
	BlobContainerName string `json:"blobContainerName"`
}

func SetUpServer() {
	router := gin.Default()
	router.POST("/camera", addCamera)
	router.GET("/ping", ping)
	fmt.Println("Starting API server.")
	err := router.Run(":8080")
	if err != nil {
		log.Print(err)
	}
}

func ping(c *gin.Context) {
	c.JSON(http.StatusOK, "pong")
}

func addCamera(c *gin.Context) {
	var cameraRequest addCameraRequest
	if err := c.ShouldBindJSON(&cameraRequest); err != nil {
		c.JSON(http.StatusBadRequest, err)
	}
	fmt.Println()
	err := k8s.CreateYoloPod(c, cameraRequest.BlobContainerName, cameraRequest.CCTVId)
	if err != nil {
		c.JSON(http.StatusInternalServerError, err)
	}
	c.JSON(http.StatusOK, "camera added")
}
