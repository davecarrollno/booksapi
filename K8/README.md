These are a set of experimental kubernetes manifests for
playing with an api app in my Minikube environment. Please
do not use this for anything critical.

Start up Minikube on your Mac.
Make sure the Ingress add-on is enabled.
Start up minikube tunnel.
Get your Minikube IP and update your /etc/hosts file to point that IP to apitest.oreilly.com.
Flush your Mac DNS.
First run: kubectl apply -f books-ns.yaml to set up the namespace.
Then, run kubectl apply -f . to start up the various pods and services.
