
/* fc.c: FlowChain measurement tools for my benchmark */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <sys/poll.h>
#include <sys/time.h>
#include <sys/stat.h>
#include <arpa/inet.h>
#include <pthread.h>
#include <linux/limits.h>


#ifndef UNIX_PATH_MAX
#define UNIX_PATH_MAX 108
#endif


#define pr_info(fmt, ...) fprintf(stdout, "%s: " fmt, \
                                  __func__, ##__VA_ARGS__)

#define pr_warn(fmt, ...) fprintf(stdout, "\x1b[1m\x1b[31m"     \
                                  "%s:WARN: " fmt "\x1b[0m",    \
                                  __func__, ##__VA_ARGS__)

#define pr_err(fmt, ...) fprintf(stderr, "%s:ERR: " fmt,        \
                                 __func__, ##__VA_ARGS__)

#define tv2l(t) ((t).tv_sec * 1000000 + (t).tv_usec)



static int caught_signal = 0;

void sig_handler(int sig)
{
        if (sig == SIGINT)
                caught_signal = 1;
}



/* structure describing this process */
struct fc {
	int mode;	
#define FC_MODE_TX	1
#define FC_MODE_RX	2
	
	int interval;	/* probe interval in usec */

	int ttl;	/* TTL when probe packet sent */
	struct in_addr src, dst;
	int port;

	int accept_mode;
	char un_path[UNIX_PATH_MAX];

	struct in_addr fc_addr; /* flowchain REST address */

	int print_when_ttl_changed;
	int print_result_budget;
};


struct fc_probe {
	uint32_t seq;
	struct timeval ts;
};


int fc_tx(struct fc fc) {

	/* make socket with specified TTL and dst port,
	 * and send probe packets every interval */

	int sock, rc;
	struct sockaddr_in sin;
	struct fc_probe probe;
	char da[16], sa[16];

	inet_ntop(AF_INET, &fc.dst, da, sizeof(da));
	inet_ntop(AF_INET, &fc.src, sa, sizeof(sa));

	pr_info("TX mode, dst %s, src %s, Port %d, TTL %d, Interval %dusec\n",
		da, sa, fc.port, fc.ttl, fc.interval);

	sock = socket(AF_INET, SOCK_DGRAM, 0);
	if (socket < 0) {
		pr_err("failed to create socket\n");

		perror("socket");
		return -1;
	}
	
	if (setsockopt(sock, IPPROTO_IP, IP_TTL,
		       &fc.ttl, sizeof(fc.ttl)) != 0) {
		pr_err("failed to set TTL\n");
		perror("setsockopt");
		return -1;
	}

	memset(&sin, 0, sizeof(sin));
	sin.sin_family = AF_INET;
	sin.sin_port = 0;
	sin.sin_addr = fc.src;
	if (bind(sock, (struct sockaddr *)&sin, sizeof(sin)) < 0) {
		pr_err("bind for tx socket failed\n");
		perror("bind");
		return -1;
	}

	memset(&sin, 0, sizeof(sin));
	sin.sin_family = AF_INET;
	sin.sin_port = htons(fc.port);
	sin.sin_addr = fc.dst;

	memset(&probe, 0, sizeof(probe));

	while(1) {
		probe.seq++;
		gettimeofday(&probe.ts, NULL);
		rc = sendto(sock, &probe, sizeof(probe), 0,
			    (struct sockaddr *)&sin, sizeof(sin));
		if (rc < 0) {
			perror("sendto");
			return -1;
		}

		usleep(fc.interval);
	}

	return 0;
}


int find_recv_ttl(struct msghdr *msg)
{
	struct cmsghdr *cmsg;
	int *ttlptr;

	for (cmsg = CMSG_FIRSTHDR(msg); cmsg != NULL;
	     cmsg = CMSG_NXTHDR(msg, cmsg)) {
		if (cmsg->cmsg_level == IPPROTO_IP &&
		    cmsg->cmsg_type == IP_TTL) {
			ttlptr = (int *)CMSG_DATA(cmsg);
			return *ttlptr;
		}
	}
	return 0;
}

int fc_rx(struct fc fc)
{

	/* make socket boudn to specified src and port,
	 * and receive and dump packets */

	int sock, rc, v = 1;
	int ttl, last_ttl = 0;
	struct sockaddr_in sin;
	struct fc_probe *probe;
	struct timeval tv;
	char dbuf[1024];
	char cbuf[1024];
	
	struct msghdr msg;
	struct iovec iov;
	struct pollfd x;
	int budget;

	memset(&sin, 0, sizeof(sin));
	sin.sin_family = AF_INET;
	sin.sin_port = htons(fc.port);
	sin.sin_addr = fc.src;

	sock = socket(AF_INET, SOCK_DGRAM, 0);
	if (socket < 0) {
		pr_err("failed to create socket\n");
		perror("socket\n");
		return -1;
	}

	if (bind(sock, (struct sockaddr *)&sin, sizeof(sin)) < 0) {
		pr_err("failed to bind\n");
		perror("bind");
		return -1;
	}

	if (setsockopt(sock, IPPROTO_IP, IP_RECVTTL, &v, sizeof(v)) < 0) {
		pr_err("failed to set IP_RECVTTL\n");
		perror("setsockopt");
		return -1;
	}

	/* setup recv buffer */
	iov.iov_base = dbuf;
	iov.iov_len = sizeof(dbuf);
	msg.msg_iov = &iov;
	msg.msg_iovlen = 1;
	msg.msg_control = cbuf;
	msg.msg_controllen = sizeof(cbuf);
	msg.msg_name = NULL;
	msg.msg_namelen = 0;
	probe = (struct fc_probe *)dbuf;

	x.fd = sock;
	x.events = POLLIN;

	printf("start to recvmsg\n");
	while(1) {
		if (caught_signal)
			break;

		poll(&x, 1, 1000);
		if (!x.revents & POLLIN)
			continue;

		rc = recvmsg(sock, &msg, 0);
		gettimeofday(&tv, NULL);
		if (rc < 0) {
			perror("recvmsg\n");
			return -1;
		}

		ttl = find_recv_ttl(&msg);

		if (fc.print_when_ttl_changed) {
			if (ttl != last_ttl) {
				/* ttl is changed */
				budget = fc.print_result_budget;
			} 

			if (budget-- > 0) {
				/* if ttl is unchanged, print this
				 * untill budget becomes empty */
				printf("TS=%ld TTL=%d DIFF=%ld\n",
				       tv2l(tv), ttl,
				       tv2l(tv) - tv2l(probe->ts));
			}
		} else {
			printf("TS=%ld TTL=%d DIFF=%ld\n",
			       tv2l(tv), ttl,
			       tv2l(tv) - tv2l(probe->ts));
		}
		last_ttl = ttl;
	}
		
	close(sock);
	return 0;
}

int fc_url_get(char *url, struct fc *fc)
{
	int sock, rc;
	char buf[2048];
	struct sockaddr_in sin;
	struct timeval before, after;

	sock = socket(AF_INET, SOCK_STREAM, 0);
	if (sock < 0) {
		pr_err("failed to create http socket\n");
		perror("socket");
	}

	sin.sin_family = AF_INET;
	sin.sin_addr = fc->fc_addr;
	sin.sin_port = htons(5000); /* Skimped hard coding... */
	
	if (connect(sock, (struct sockaddr*)&sin, sizeof(sin)) < 0) {
		pr_err("failed to connect flowchain REST addr\n");
		perror("connect");
		return -1;
	}

	snprintf(buf, sizeof(buf), "GET %s\r\n", url);
	gettimeofday(&before, NULL);
	rc = write(sock, buf, strlen(buf));
	gettimeofday(&after, NULL);
	if (rc < 0) {
		perror("write");
		return rc;
	}

	printf("TS=%ld START=%ld END=%ld DIFF=%ld URL=%s\n",
	       tv2l(after), tv2l(before), tv2l(after),
	       tv2l(after) - tv2l(before), url);

	close(sock);

	return 0;
}

int fc_ctl(char *buf, struct fc *fc)
{
	/* process cmd string.
	 * syntax is : [CMD] [STRING]
	 * - 1. GET [URL]
	 * - 2. ECHO [STRING]
	 */

	char *cmd, *str, *p;
	struct timeval tv;

	/* parse buf */
	for (p = buf; *p != '\0'; p++) {
		if (*p == '\n') *p = '\0';
	}
	for (cmd = buf, str = buf; *str != ' ' && *str != '\0'; str++);
	for (; *str == ' '; str++) *str = '\0';


	if (strncmp(cmd, "GET", 3) == 0) {
		/* send GET request to specified URL */
		fc_url_get(str, fc);

	} else if (strncmp(cmd, "ECHO", 4) == 0) {
		/* echo string to stdout */
		gettimeofday(&tv, NULL);
		printf("TS=%ld ECHO %s\n", tv2l(tv), str);

	} else {
		gettimeofday(&tv, NULL);
		printf("TS=%ld ERROR invalid command '%s'\n", tv2l(tv), cmd);
		return -1;
	}

	return 0;
}


void * fc_ctl_thread(void *param)
{
	struct fc *fc = param;
	int sock, a_sock, s_sock, rc;
	struct sockaddr_un sun;
	char buf[2048];
	struct pollfd x;

	

	sock = socket(AF_UNIX, fc->accept_mode ? SOCK_STREAM : SOCK_DGRAM, 0);
	if (sock < 0) {
		pr_err("failed to create unix domain socket for control\n");
		perror("socket");
		return NULL;
	}
	       
	unlink(fc->un_path);
	memset(&sun, 0, sizeof(sun));
	sun.sun_family = AF_UNIX;
	strncpy(sun.sun_path, fc->un_path, UNIX_PATH_MAX);
	if (bind(sock, (struct sockaddr*)&sun, sizeof(sun)) < 0) {
		pr_err("failed to bind unix socket to '%s'", fc->un_path);
		perror("bind");
		close(sock);
		return NULL;
	}

	if (chmod(fc->un_path, S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP
		  | S_IROTH | S_IWOTH) < 0) {
		pr_err("failed to chmod %s", fc->un_path);
		close(sock);
		return NULL;
	}


	listen(sock, 1);
	s_sock = sock;

	while(1) {

		if (caught_signal)
			break;

		x.fd = sock;
		x.events = POLLIN;
		x.revents = 0;

		/* timeout 1sec */
		if (poll(&x, 1, 1000) < 0) {
			pr_err("poll failed\n");
			perror("poll");
			return NULL;
		}

		if (!x.revents & POLLIN)
			continue;

		if (fc->accept_mode && sock == s_sock) {
			a_sock = accept(sock, NULL, 0);
			sock = a_sock;
		}

		rc = read(sock, buf, sizeof(buf));
		if (rc == 0 && fc->accept_mode) {
			close(sock);
			sock = s_sock;
			continue;
		} else if (rc < 0) {
			perror("read");
			continue;
		}
		fc_ctl(buf, fc);
	}

	close(sock);
	if (fc->accept_mode)
		close(s_sock);
		

	return NULL;
}

void usage(void) {
	printf("fc usage:\n"
	       "\t -m: fc probe mode (rx|tx)\n"
	       "\t -d: dst address (in TX mode)\n"
	       "\t -s: src address (in TX mode)\n"
	       "\t -b: bind address (in RX mode)\n"
	       "\t -i: probe interval (usec), default 1000 usec (1msec)\n"
	       "\t -p: port number, default 60000\n"
	       "\t -t: TTL of probe packets, default 64\n"
	       "\t -u: control unix domain socket path, default /tmp/fc.sock\n"
	       "\t -f: FlowChain address\n"
	       "\t -T: print if TTL is changed\n"
		);
}


int main(int argc, char **argv)
{
	int ch, rc;
	struct fc fc;
	pthread_t tid;

	memset(&fc, 0, sizeof(fc));
	fc.mode = 0;
	fc.interval = 1000;
	fc.port = 60000;
	fc.ttl = 64;
	fc.print_when_ttl_changed = 0;
	fc.print_result_budget = 1;
	strncpy(fc.un_path, "/tmp/fc.sock", UNIX_PATH_MAX);
	
	while ((ch = getopt(argc, argv, "m:d:s:b:i:p:t:u:af:TB:")) != -1) {
		switch (ch) {
		case 'm' :
			if (strncmp(optarg, "tx", 2) == 0)
				fc.mode = FC_MODE_TX;
			else if (strncmp(optarg, "rx", 2) == 0)
				fc.mode = FC_MODE_RX;
			else {
				pr_err("invalid mode '%s'\n", optarg);
				return -1;
			}
			break;

		case 'd' :
			if (inet_pton(AF_INET, optarg, &fc.dst) < 1) {
				pr_err("invalid destination address '%s'\n",
					optarg);
				return -1;
			}
			break;
			
		case 's' :
			if (inet_pton(AF_INET, optarg, &fc.src) < 1) {
				pr_err("invalid source address '%s'\n",
				       optarg);
				return -1;
			}
			break;

		case 'b' :
			if (inet_pton(AF_INET, optarg, &fc.src) < 1) {
				pr_err("invalid bind address '%s'\n", optarg);
				return -1;
			}
			break;

		case 'i' :
			fc.interval = atoi(optarg);
			break;

		case 'p' :
			fc.port = atoi(optarg);
			break;

		case 't' :
			fc.ttl = atoi(optarg);
			break;

		case 'u' :
			strncpy(fc.un_path, optarg, UNIX_PATH_MAX);
			break;

		case 'a' :
			fc.accept_mode = 1;
			break;

		case 'f' :
			if (inet_pton(AF_INET, optarg, &fc.fc_addr) < 1) {
				pr_err("invalid flowchain address '%s'\n",
				       optarg);
				return -1;
			}
			break;

		case 'T' :
			fc.print_when_ttl_changed = 1;
			break;

		case 'B' :
			fc.print_result_budget = atoi(optarg);
			break;

		default :
			usage();
			return -1;
		}
	}

	switch (fc.mode) {
	case 0 :
		pr_err("please specify mode '-m tx|rx'\n");
		return -1;

	case FC_MODE_TX :
		return fc_tx(fc);
		break;

	case FC_MODE_RX :

		if (signal(SIGINT, sig_handler) == SIG_ERR) {
			perror("cannot set signal\n");
			return -1;
		}

		rc = pthread_create(&tid, NULL, fc_ctl_thread, &fc);
		if (rc < 0) {
			perror("pthread_create");
			return -1;
		}

		fc_rx(fc);
		pthread_join(tid, NULL);
		break;

	default :
		pr_err("invalid mode\n");
		return -1;
	}
	

	return 0; /* not reached */
}
