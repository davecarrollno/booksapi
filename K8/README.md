These are a set of experimental kubernetes manifests for playing with an api app in my Minikube environment. Please do not use this for anything critical.

# Instructions
* Start up Minikube on your Mac.
* Make sure the Ingress add-on is enabled.
* Start up Minikube Tunnel
* Find your Minikube IP and add that to your hosts file
* Set <your minikube ip> apitest.oreilly.com in your hosts file
	* flush dns
* First run kubectl apply -f books-ns.yaml to create the namespace
* Then, run kubectl apply -f . to start up the pods and services.
