--
-- PostgreSQL database dump
--

-- Dumped from database version 16.2
-- Dumped by pg_dump version 16.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: meal_type; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.meal_type AS ENUM (
    'Breakfast',
    'Lunch',
    'Dinner',
    'Snack'
);


ALTER TYPE public.meal_type OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: achievements; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.achievements (
    achievementid integer NOT NULL,
    userid integer,
    achievementname character varying(100),
    achievementdescription text,
    achievementdate date
);


ALTER TABLE public.achievements OWNER TO postgres;

--
-- Name: forumcomments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.forumcomments (
    commentid integer NOT NULL,
    text text NOT NULL,
    postid integer
);


ALTER TABLE public.forumcomments OWNER TO postgres;

--
-- Name: forumcomments_commentid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.forumcomments_commentid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.forumcomments_commentid_seq OWNER TO postgres;

--
-- Name: forumcomments_commentid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.forumcomments_commentid_seq OWNED BY public.forumcomments.commentid;


--
-- Name: forumposts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.forumposts (
    postid integer NOT NULL,
    title character varying(255) NOT NULL,
    description text
);


ALTER TABLE public.forumposts OWNER TO postgres;

--
-- Name: forumposts_postid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.forumposts_postid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.forumposts_postid_seq OWNER TO postgres;

--
-- Name: forumposts_postid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.forumposts_postid_seq OWNED BY public.forumposts.postid;


--
-- Name: friends; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.friends (
    friendshipid integer NOT NULL,
    userid1 integer,
    userid2 integer
);


ALTER TABLE public.friends OWNER TO postgres;

--
-- Name: macrotracker; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.macrotracker (
    trackerid integer NOT NULL,
    userid integer,
    logtime time without time zone,
    name character varying(100),
    caloriesconsumed integer,
    proteinconsumed double precision,
    carbsconsumed double precision,
    fatsconsumed double precision,
    meal_type public.meal_type,
    target_caloriesconsumed double precision,
    target_proteinconsumed double precision,
    target_carbsconsumed double precision,
    target_fatsconsumed double precision
);


ALTER TABLE public.macrotracker OWNER TO postgres;

--
-- Name: macrotracker_trackerid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.macrotracker_trackerid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.macrotracker_trackerid_seq OWNER TO postgres;

--
-- Name: macrotracker_trackerid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.macrotracker_trackerid_seq OWNED BY public.macrotracker.trackerid;


--
-- Name: messages; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.messages (
    messageid integer NOT NULL,
    senderuserid integer,
    receiveruserid integer,
    messagecontent text,
    "timestamp" timestamp without time zone
);


ALTER TABLE public.messages OWNER TO postgres;

--
-- Name: nutritionlog; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.nutritionlog (
    logid integer NOT NULL,
    userid integer,
    fooditem character varying(100),
    quantity double precision,
    caloriesconsumed integer,
    logdate date
);


ALTER TABLE public.nutritionlog OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    userid integer NOT NULL,
    username character varying(50) NOT NULL,
    password character varying(100) NOT NULL,
    email character varying(100) NOT NULL,
    firstname character varying(50),
    lastname character varying(50),
    dateofbirth date,
    gender character varying(10),
    height double precision,
    weight double precision,
    joindate timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT users_gender_check CHECK (((gender)::text = ANY ((ARRAY['Male'::character varying, 'Female'::character varying, 'Other'::character varying])::text[])))
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_userid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_userid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_userid_seq OWNER TO postgres;

--
-- Name: users_userid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_userid_seq OWNED BY public.users.userid;


--
-- Name: userstats; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.userstats (
    userid integer NOT NULL,
    dailycaloriesintake integer,
    totalsteps integer,
    totaldistance double precision,
    totalworkouts integer,
    lastactivedate timestamp without time zone
);


ALTER TABLE public.userstats OWNER TO postgres;

--
-- Name: workouthistory; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.workouthistory (
    workoutid integer NOT NULL,
    userid integer,
    workouttype character varying(50),
    duration integer,
    caloriesburned double precision,
    startdatetime timestamp without time zone,
    enddatetime timestamp without time zone
);


ALTER TABLE public.workouthistory OWNER TO postgres;

--
-- Name: forumcomments commentid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.forumcomments ALTER COLUMN commentid SET DEFAULT nextval('public.forumcomments_commentid_seq'::regclass);


--
-- Name: forumposts postid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.forumposts ALTER COLUMN postid SET DEFAULT nextval('public.forumposts_postid_seq'::regclass);


--
-- Name: macrotracker trackerid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.macrotracker ALTER COLUMN trackerid SET DEFAULT nextval('public.macrotracker_trackerid_seq'::regclass);


--
-- Name: users userid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN userid SET DEFAULT nextval('public.users_userid_seq'::regclass);


--
-- Data for Name: achievements; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.achievements (achievementid, userid, achievementname, achievementdescription, achievementdate) FROM stdin;
\.


--
-- Data for Name: forumcomments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.forumcomments (commentid, text, postid) FROM stdin;
\.


--
-- Data for Name: forumposts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.forumposts (postid, title, description) FROM stdin;
\.


--
-- Data for Name: friends; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.friends (friendshipid, userid1, userid2) FROM stdin;
\.


--
-- Data for Name: macrotracker; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.macrotracker (trackerid, userid, logtime, name, caloriesconsumed, proteinconsumed, carbsconsumed, fatsconsumed, meal_type, target_caloriesconsumed, target_proteinconsumed, target_carbsconsumed, target_fatsconsumed) FROM stdin;
1	8	\N	ass	600	200	200	200	Breakfast	\N	\N	\N	\N
2	8	\N	Costco Pizza	3000	180	180	180	Breakfast	\N	\N	\N	\N
3	10	\N	Ass	1000	100	100	100	Breakfast	\N	\N	\N	\N
\.


--
-- Data for Name: messages; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.messages (messageid, senderuserid, receiveruserid, messagecontent, "timestamp") FROM stdin;
\.


--
-- Data for Name: nutritionlog; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.nutritionlog (logid, userid, fooditem, quantity, caloriesconsumed, logdate) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (userid, username, password, email, firstname, lastname, dateofbirth, gender, height, weight, joindate) FROM stdin;
1	morbing123	$2b$12$7lZpVKkhatBlV0/uTWnGKuIjVqQgPeczT3N8eSZy73tfVXy7m6BhW	andrew5@gmail.com	john	madden	1990-04-25	Male	185	250	2024-04-20 17:46:48.987651
2	shubismom	$2b$12$jBPmOA5/HeD0B3EU9xLB9OBtvHWOzS15zHYobyLmjNUmldJVNX6ES	memes123@gmail.com	shubis	mom	\N	\N	\N	\N	2024-04-20 17:53:07.660946
3	shimadubai	$2b$12$udxRxNvUT6Y8TFTIVNRAkOahVFZ3GuWLp.HhkQvBLYfTawR.2ApqO	shima123@gmail.com	sdhufuisdlfh	hjshdjsdhjshd	\N	\N	\N	\N	2024-04-20 17:59:07.506622
4	shubbb123	$2b$12$5jj9UTqnWFpHXeWTiqQ.FO8XHWX7mZ1mu29Erz81DoNhODMFzJ3wK	shubi@gmail.com	shubi	doobie	\N	\N	\N	\N	2024-04-20 18:00:33.398715
5	shubii	$2b$12$iK9cdZNkniWE.fRMNa9ZMe3YGXYZAEUzZ3357DDwoshdeSZ7DCJTm	shubi@edible.com	Shub	shub	2001-09-11	Male	50	4000	2024-04-20 18:00:59.159744
6	latino123	$2b$12$yPeopv41LC8rfppxM/cdSe/m9HcXSzvIUcsb9RT1tnTWRl7F361.e	jacob@gmail.com	jacob	garcia	1999-04-20	Male	180	80	2024-04-20 23:22:38.129885
7	squidgames	$2b$12$SWT/9KXzPdRK6x.KQBqTNODUauSPz9jXj3jB1TB9100HW7fbuWahq	andrew7@gmail.com	john	madden	1997-04-20	Male	73	240	2024-04-23 15:02:04.693997
8	obama	$2b$12$QkyJCwOvPrrnAGPR19RqLe67Msv/nGjWM5I83C1ObbRSisO8c1UbC	obama@gmail.com	obamas	MOM	1997-04-20	Male	180	240	2024-04-26 20:36:19.331436
9	andrew	$2b$12$uf8UnnXpkNtwXLgCYzbaZuEAHGxxz4FyKytT99fs3cKWjdu5bnwVK	andrew@gmail.com	andrew	meme	\N	\N	\N	\N	2024-04-27 02:11:00.492561
10	jacob	$2b$12$eyUdPxS3qmzS9B9qhlN2zeEw69smn5vY8hr6SvOzcNIGEf/zTuw5.	jacob123@gmail.com	jacob	garcia	1997-04-20	Male	72	110	2024-04-27 18:20:15.883715
\.


--
-- Data for Name: userstats; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.userstats (userid, dailycaloriesintake, totalsteps, totaldistance, totalworkouts, lastactivedate) FROM stdin;
\.


--
-- Data for Name: workouthistory; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.workouthistory (workoutid, userid, workouttype, duration, caloriesburned, startdatetime, enddatetime) FROM stdin;
\.


--
-- Name: forumcomments_commentid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.forumcomments_commentid_seq', 1, false);


--
-- Name: forumposts_postid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.forumposts_postid_seq', 1, false);


--
-- Name: macrotracker_trackerid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.macrotracker_trackerid_seq', 3, true);


--
-- Name: users_userid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_userid_seq', 10, true);


--
-- Name: achievements achievements_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.achievements
    ADD CONSTRAINT achievements_pkey PRIMARY KEY (achievementid);


--
-- Name: forumcomments forumcomments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.forumcomments
    ADD CONSTRAINT forumcomments_pkey PRIMARY KEY (commentid);


--
-- Name: forumposts forumposts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.forumposts
    ADD CONSTRAINT forumposts_pkey PRIMARY KEY (postid);


--
-- Name: forumposts forumposts_title_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.forumposts
    ADD CONSTRAINT forumposts_title_key UNIQUE (title);


--
-- Name: friends friends_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.friends
    ADD CONSTRAINT friends_pkey PRIMARY KEY (friendshipid);


--
-- Name: macrotracker macrotracker_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.macrotracker
    ADD CONSTRAINT macrotracker_pkey PRIMARY KEY (trackerid);


--
-- Name: messages messages_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_pkey PRIMARY KEY (messageid);


--
-- Name: nutritionlog nutritionlog_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.nutritionlog
    ADD CONSTRAINT nutritionlog_pkey PRIMARY KEY (logid);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (userid);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: userstats userstats_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.userstats
    ADD CONSTRAINT userstats_pkey PRIMARY KEY (userid);


--
-- Name: workouthistory workouthistory_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workouthistory
    ADD CONSTRAINT workouthistory_pkey PRIMARY KEY (workoutid);


--
-- Name: achievements achievements_userid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.achievements
    ADD CONSTRAINT achievements_userid_fkey FOREIGN KEY (userid) REFERENCES public.users(userid);


--
-- Name: userstats fk_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.userstats
    ADD CONSTRAINT fk_user FOREIGN KEY (userid) REFERENCES public.users(userid);


--
-- Name: forumcomments forumcomments_postid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.forumcomments
    ADD CONSTRAINT forumcomments_postid_fkey FOREIGN KEY (postid) REFERENCES public.forumposts(postid);


--
-- Name: friends friends_userid1_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.friends
    ADD CONSTRAINT friends_userid1_fkey FOREIGN KEY (userid1) REFERENCES public.users(userid);


--
-- Name: friends friends_userid2_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.friends
    ADD CONSTRAINT friends_userid2_fkey FOREIGN KEY (userid2) REFERENCES public.users(userid);


--
-- Name: macrotracker macrotracker_userid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.macrotracker
    ADD CONSTRAINT macrotracker_userid_fkey FOREIGN KEY (userid) REFERENCES public.users(userid);


--
-- Name: messages messages_receiveruserid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_receiveruserid_fkey FOREIGN KEY (receiveruserid) REFERENCES public.users(userid);


--
-- Name: messages messages_senderuserid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_senderuserid_fkey FOREIGN KEY (senderuserid) REFERENCES public.users(userid);


--
-- Name: nutritionlog nutritionlog_userid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.nutritionlog
    ADD CONSTRAINT nutritionlog_userid_fkey FOREIGN KEY (userid) REFERENCES public.users(userid);


--
-- Name: workouthistory workouthistory_userid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workouthistory
    ADD CONSTRAINT workouthistory_userid_fkey FOREIGN KEY (userid) REFERENCES public.users(userid);


--
-- PostgreSQL database dump complete
--

