dist=$(tr -s ' \011' '\012' < /etc/issue | head -n 1)
if [ "$dist" = "Ubuntu" ]
then
  apt-get -y install ruby
  gem install redis
else
  gpg2 --keyserver hkp://keys.gnupg.net --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3
  curl -L get.rvm.io | bash -s stable
  source /etc/profile.d/rvm.sh 
  rvm install 2.3.1
  rvm use 2.3.1 --default
  gem install redis
fi

