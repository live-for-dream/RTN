#include <RTN_event.h>

int RTN_event_init() {
	int epfd = epoll_create(RTN_EVENT_MAX_SIZE);
	
}