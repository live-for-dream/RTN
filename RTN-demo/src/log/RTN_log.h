#include <RTN_error.h>
#include <zlog.h>

typedef zlog_category_t RTN_log_t; 

#define RTN_debug(cat, format, args...) 	zlog_debug(cat, format, ##args)
#define RTN_info(cat, format, args...) 		zlog_info(cat, format, ##args)
#define RTN_notice(cat, format, args...) 	zlog_notice(cat, format, ##args)
#define RTN_warn(cat, format, args...) 		zlog_warn(cat, format, ##args)
#define RTN_fatal(cat, format, args...) 	zlog_fatal(cat, format, ##args)
#define RTN_error(cat, format, args...) 	zlog_error(cat, format, ##args)

RTN_log_t * RTN_log_init(const char * conf, const char * category);
#define RTN_log_fini() zlog_fini()
