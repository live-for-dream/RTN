#inclulde <sys/epoll.h>

#define RTN_EVENT_MAX_SIZE 65536
typedef int (*event_handler_t)(void * data);
typedef struct epoll_event rtn_ev_t;
typedef struct rtn_ev_data_s {
	void 			*data;//point to RTN_conn_t
	event_handler_t  handler;//
	int				 fd;
	int				 epfd;
} rtn_ev_data_t;

#define RTN_ADD_READ_EVENT(fd, ep_fd, EPOLL_CTL_ADD, ev) \
	(ev)->events = EPOLLIN | | EPOLLET; \
	epoll_ctl(ep_fd, EPOLL_CTL_ADD, fd, ev)

#define RTN_EVENT_ADD_DATA(ev, data) \
		(ev)->data.ptr = (void *)(data)

#define RTN_EVENT_GET_DATA(ev) \
		(rtn_ev_data_t *)((ev)->data.ptr)
		
#define RTN_ADD_READ_EVENT(fd, ep_fd, EPOLL_CTL_ADD, ev) \
		(ev)->events = EPOLLIN | EPOLLET; \
		epoll_ctl(ep_fd, EPOLL_CTL_ADD, fd, ev)

#define RTN_ADD_WRITE_EVENT(fd, ep_fd, EPOLL_CTL_ADD, ev) \
		(ev)->events = EPOLLOUT | EPOLLET; \
		epoll_ctl(ep_fd, EPOLL_CTL_ADD, fd, ev)

#define RTN_ADD_RW_EVENT(fd, ep_fd, EPOLL_CTL_ADD, ev) \
		(ev)->events = EPOLLOUT | EPOLLIN | EPOLLET; \
		epoll_ctl(ep_fd, EPOLL_CTL_ADD, fd, ev)

#define RTN_GET_EV_DATA(ev, d) \
		(d) = (rtn_ev_data_t *)(ev)->data.ptr
		

int RTN_event_init();	
