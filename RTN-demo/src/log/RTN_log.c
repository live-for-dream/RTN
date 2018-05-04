#include <RTN_log.h>

RTN_log_t * RTN_log_init(const char * conf, const char * category) {
	int cf;
	RTN_log_t *log;
	
	if (conf == NULL || category == NULL) {
		printf("init failed, conf or category is null\n");
		return NULL;
	}
	
	cf = zlog_init(conf);
	if (cf) {
		printf("init failed\n");
        return NULL;
	}

	log = zlog_get_category(category);
	if (!log) {
		printf("init failed, get category failed\n");
		zlog_fini();
		return NULL;
	}
}

