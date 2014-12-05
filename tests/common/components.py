from common.integration import FileAssertHelper
from common.integration import TextFileAssertHelper


class BuildPackAssertHelper(object):
    """Helper to assert build pack is working"""

    def assert_start_script_is_correct(self, build_dir):
        fah = FileAssertHelper()
        fah.expect().path(build_dir, 'start.sh').exists()
        tfah = TextFileAssertHelper()
        (tfah.expect()
            .on_file(build_dir, 'start.sh')
            .line(0)
                .equals('export PYTHONPATH=$HOME/.bp/lib\n')  # noqa
            .any_line()
                .equals('$HOME/.bp/bin/rewrite "$HOME/.env"\n')
            .line(-1)
                .equals('$HOME/.bp/bin/start'))

    def assert_scripts_are_installed(self, build_dir):
        fah = FileAssertHelper()
        (fah.expect()
            .path(build_dir, '.bp', 'bin', 'rewrite')
            .root(build_dir, '.bp', 'lib', 'build_pack_utils')
                .directory_count_equals(22)  # noqa
                .path('utils.py')
                .path('process.py')
            .exists())

    def assert_config_options(self, build_dir):
        fah = FileAssertHelper()
        (fah.expect()
            .path(build_dir, '.bp-config', 'options.json')
            .exists())


class PhpAssertHelper(object):
    """Helper to assert PHP is installed & configured correctly"""

    def assert_start_script_is_correct(self, build_dir):
        fah = FileAssertHelper()
        fah.expect().path(build_dir, 'start.sh').exists()
        tfah = TextFileAssertHelper()
        (tfah.expect()
            .on_file(build_dir, 'start.sh')
            .any_line()
            .equals('$HOME/.bp/bin/rewrite "$HOME/php/etc"\n'))

    def assert_contents_of_procs_file(self, build_dir):
        fah = FileAssertHelper()
        fah.expect().path(build_dir, '.procs').exists()
        tfah = TextFileAssertHelper()
        (tfah.expect()
            .on_file(build_dir, '.procs')
            .any_line()
                .equals('php-fpm: $HOME/php/sbin/php-fpm -p '  # noqa
                        '"$HOME/php/etc" -y "$HOME/php/etc/php-fpm.conf"'
                        ' -c "$HOME/php/etc"\n')
                .equals('php-fpm-logs: tail -F $HOME/logs/php-fpm.log\n'))

    def assert_contents_of_env_file(self, build_dir):
        fah = FileAssertHelper()
        fah.expect().path(build_dir, '.env').exists()
        tfah = TextFileAssertHelper()
        (tfah.expect()
            .on_file(build_dir, '.env')
            .any_line()
                .equals('PATH=@PATH:@HOME/php/bin\n')  # noqa
                .equals('LD_LIBRARY_PATH=@LD_LIBRARY_PATH:@HOME/php/lib\n'))

    def assert_files_installed(self, build_dir):
        fah = FileAssertHelper()
        (fah.expect()
            .root(build_dir, 'php')
                .path('etc', 'php-fpm.conf')  # noqa
                .path('etc', 'php.ini')
                .path('sbin', 'php-fpm')
                .path('bin')
            .root(build_dir, 'php', 'lib', 'php', 'extensions',
                  'no-debug-non-zts-20100525')
                .path('bz2.so')
                .path('zlib.so')
                .path('curl.so')
                .path('mcrypt.so')
            .exists())


class HttpdAssertHelper(object):
    """Helper to assert HTTPD is installed and configured correctly"""

    def assert_start_script_is_correct(self, build_dir):
        fah = FileAssertHelper()
        fah.expect().path(build_dir, 'start.sh').exists()
        tfah = TextFileAssertHelper()
        (tfah.expect()
            .on_file(build_dir, 'start.sh')
            .any_line()
            .equals('$HOME/.bp/bin/rewrite "$HOME/httpd/conf"\n'))

    def assert_downloads_from_output(self, output):
        tfah = TextFileAssertHelper()
        (tfah.expect()
            .on_string(output)
            .line_count_equals(21, lambda l: l.startswith('Downloaded'))
            .line_count_equals(2, lambda l: l.startswith('Installing'))
            .line(-1).startswith('Finished:'))

    def assert_contents_of_procs_file(self, build_dir):
        fah = FileAssertHelper()
        fah.expect().path(build_dir, '.procs').exists()
        tfah = TextFileAssertHelper()
        (tfah.expect()
            .on_file(build_dir, '.procs')
            .any_line()
                .equals('httpd: $HOME/httpd/bin/apachectl -f '  # noqa
                        '"$HOME/httpd/conf/httpd.conf" -k start '
                        '-DFOREGROUND\n'))

    def assert_contents_of_env_file(self, build_dir):
        fah = FileAssertHelper()
        fah.expect().path(build_dir, '.env').exists()
        tfah = TextFileAssertHelper()
        (tfah.expect()
            .on_file(build_dir, '.env')
            .any_line()
            .equals('HTTPD_SERVER_ADMIN=dan@mikusa.com\n'))

    def assert_web_dir_exists(self, build_dir, web_dir):
        fah = FileAssertHelper()
        (fah.expect()
            .path(build_dir, web_dir)
            .exists())

    def assert_files_installed(self, build_dir):
        fah = FileAssertHelper()
        (fah.expect()
            .root(build_dir, 'httpd', 'conf')
                .path('httpd.conf')  # noqa
                .root('extra')
                    .path('httpd-modules.conf')  # noqa
                    .path('httpd-remoteip.conf')
            .root(build_dir, 'httpd', 'modules', reset=True)
                .path('mod_authz_core.so')
                .path('mod_authz_host.so')
                .path('mod_dir.so')
                .path('mod_env.so')
                .path('mod_log_config.so')
                .path('mod_mime.so')
                .path('mod_mpm_event.so')
                .path('mod_proxy.so')
                .path('mod_proxy_fcgi.so')
                .path('mod_reqtimeout.so')
                .path('mod_unixd.so')
                .path('mod_remoteip.so')
                .path('mod_rewrite.so')
            .exists())


class NginxAssertHelper(object):
    """Helper to assert Nginx is installed and configured correctly"""

    def assert_start_script_is_correct(self, build_dir):
        fah = FileAssertHelper()
        fah.expect().path(build_dir, 'start.sh').exists()
        tfah = TextFileAssertHelper()
        (tfah.expect()
            .on_file(build_dir, 'start.sh')
            .any_line()
            .equals('$HOME/.bp/bin/rewrite "$HOME/nginx/conf"\n'))

    def assert_downloads_from_output(self, output):
        tfah = TextFileAssertHelper()
        (tfah.expect()
            .on_string(output)
            .line_count_equals(7, lambda l: l.startswith('Downloaded'))
            .line_count_equals(2, lambda l: l.startswith('Installing'))
            .line(-1).startswith('Finished:'))

    def assert_contents_of_procs_file(self, build_dir):
        fah = FileAssertHelper()
        fah.expect().path(build_dir, '.procs').exists()
        tfah = TextFileAssertHelper()
        (tfah.expect()
            .on_file(build_dir, '.procs')
            .any_line()
                .equals('nginx: $HOME/nginx/sbin/nginx -c '  # noqa
                        '"$HOME/nginx/conf/nginx.conf"\n'))

    def assert_web_dir_exists(self, build_dir, web_dir):
        fah = FileAssertHelper()
        (fah.expect()
            .path(build_dir, web_dir)
            .exists())

    def assert_files_installed(self, build_dir):
        fah = FileAssertHelper()
        (fah.expect()
            .root(build_dir, 'nginx')
                .path('logs')  # noqa
                .path('sbin', 'nginx')
            .root(build_dir, 'nginx', 'conf')
                .directory_count_equals(10)
                .path('fastcgi_params')
                .path('http-logging.conf')
                .path('http-defaults.conf')
                .path('http-php.conf')
            .exists())
        tfah = TextFileAssertHelper()
        (tfah.expect()
            .on_file(build_dir, 'nginx', 'conf', 'http-php.conf')
            .any_line()
                .does_not_contain('#{PHP_FPM_LISTEN}')  # noqa
                .does_not_contain('{TMPDIR}'))
