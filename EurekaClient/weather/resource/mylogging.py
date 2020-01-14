import logging
class Logging:
    def __init__(self,path, clevel=logging.ERROR, flevel=logging.DEBUG):
        self.logger=logging.getLogger(path)
        self.logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter('%(asctime)s %(module)s %(funcName)s [line:%(lineno)d] %(levelname)s %(message)s','%Y-%m-%d %H:%M:%S')

        sh= logging.StreamHandler()
        sh.setFormatter(fmt)
        sh.setLevel(clevel)

        fh= logging.FileHandler(path)
        fh.setFormatter(fmt)
        fh.setLevel(flevel)
        self.logger.addHandler(sh)
        self.logger.addHandler(fh)

    def debug(self,message):
        self.logger.debug(message)

    def info(self,message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def warning(self, message):
        self.logger.warning(message)

    def cri(self,message):
        self.logger.critical(message)

if __name__ == '__main__':
    log=Logging('mylogtest.log',logging.ERROR,logging.DEBUG)
    log.debug('debug')
    log.info('info')
    log.error('error')
    log.warning('warning')

