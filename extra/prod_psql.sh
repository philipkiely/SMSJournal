sudo yum install -y  https://download.postgresql.org/pub/repos/yum/10/redhat/rhel-7-x86_64/pgdg-redhat10-10-2.noarch.rpm
sudo sed -i "s/rhel-\$releasever-\$basearch/rhel-latest-x86_64/g" "/etc/yum.repos.d/pgdg-10-redhat.repo"
sudo yum install -y postgresql10-devel
