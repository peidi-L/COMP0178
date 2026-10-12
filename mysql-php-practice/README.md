# MySQL + PHP practice

This small site connects PHP to the existing local MySQL server. It uses the `EstateAgent`, `Branch`, and `Staff` objects created in MySQL Workbench.

From Terminal, run:

```bash
cd ~/Desktop/COMP0178/mysql-php-practice
MYSQL_PASSWORD='your-mysql-password' php -S 127.0.0.1:8080
```

Then open <http://127.0.0.1:8080>.

Stop the PHP server with **Control-C**. The password exists only in that Terminal command/session. Do not add a real password to this folder or commit it to Git.

Optional connection settings:

```bash
MYSQL_HOST=127.0.0.1 \
MYSQL_PORT=3306 \
MYSQL_DATABASE=EstateAgent \
MYSQL_USER=root \
MYSQL_PASSWORD='your-mysql-password' \
php -S 127.0.0.1:8080
```

This uses PHP's built-in development server, so XAMPP and MariaDB are not required for this practice site.
