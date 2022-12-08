package k8s

import (
	"context"
	"fmt"
	corev1 "k8s.io/api/core/v1"
	"k8s.io/apimachinery/pkg/api/resource"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/tools/clientcmd"
)

//const kubeconfigPath = "/etc/kubeconfig"

const kubeconfigPath = "/go/kubeconfig"

//const kubeconfigPath = "/Users/pj/kubeconfig"

func connectToK8s() (*kubernetes.Clientset, error) {

	config, err := clientcmd.BuildConfigFromFlags("", kubeconfigPath)
	if err != nil {
		//log.Panicln("failed to create K8s config")
		return nil, err
	}

	clientset, err := kubernetes.NewForConfig(config)
	if err != nil {
		//log.Panicln("Failed to create K8s clientset")
		return nil, err
	}

	return clientset, nil
}

func CreateYoloPod(ctx context.Context, blobContainerLocation string, cctvId int) error {
	client, err := connectToK8s()
	if err != nil {
		return err
	}
	podName := fmt.Sprintf("cctv-%d", cctvId)
	pod := client.CoreV1().Pods("default")
	image := "docker.io/praru15/machinelearning:latest"
	cpuLimit, err := resource.ParseQuantity("1800m")
	if err != nil {
		return err
	}
	memLimit, _ := resource.ParseQuantity("4Gi")
	memRequests, _ := resource.ParseQuantity("2Gi")
	cpuRequests, _ := resource.ParseQuantity("1000m")

	podSpec := &corev1.Pod{
		ObjectMeta: metav1.ObjectMeta{
			Name:      podName,
			Namespace: "default",
		},
		Spec: corev1.PodSpec{
			Containers: []corev1.Container{
				{
					Name:            "ambulance-detector",
					Image:           image,
					ImagePullPolicy: corev1.PullIfNotPresent,
					Command:         nil,
					Args: []string{
						"python3",
						"runrun-emv-detector.py",
						blobContainerLocation,
					},
					Resources: corev1.ResourceRequirements{
						Limits: corev1.ResourceList{
							corev1.ResourceCPU:    cpuLimit,
							corev1.ResourceMemory: memLimit,
						},
						Requests: corev1.ResourceList{
							corev1.ResourceCPU:    cpuRequests,
							corev1.ResourceMemory: memRequests,
						},
					},
				},
			},
		},
	}
	_, err = pod.Create(ctx, podSpec, metav1.CreateOptions{})
	if err != nil {
		return err
	}
	return nil
}
