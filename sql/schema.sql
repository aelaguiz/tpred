--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

--
-- Name: hashtag_id_seq; Type: SEQUENCE; Schema: public; Owner: aelaguiz
--

CREATE SEQUENCE hashtag_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.hashtag_id_seq OWNER TO aelaguiz;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: hashtag; Type: TABLE; Schema: public; Owner: aelaguiz; Tablespace: 
--

CREATE TABLE hashtag (
    id bigint DEFAULT nextval('hashtag_id_seq'::regclass) NOT NULL,
    hashtag character varying NOT NULL
);


ALTER TABLE public.hashtag OWNER TO aelaguiz;

--
-- Name: tweet_id_seq; Type: SEQUENCE; Schema: public; Owner: aelaguiz
--

CREATE SEQUENCE tweet_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tweet_id_seq OWNER TO aelaguiz;

--
-- Name: post; Type: TABLE; Schema: public; Owner: aelaguiz; Tablespace: 
--

CREATE TABLE post (
    id bigint DEFAULT nextval('tweet_id_seq'::regclass) NOT NULL,
    site_post_id bigint NOT NULL,
    sn_id bigint NOT NULL,
    created_at timestamp without time zone NOT NULL,
    body_id bigint
);


ALTER TABLE public.post OWNER TO aelaguiz;

--
-- Name: post_body_id; Type: SEQUENCE; Schema: public; Owner: aelaguiz
--

CREATE SEQUENCE post_body_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.post_body_id OWNER TO aelaguiz;

--
-- Name: post_body; Type: TABLE; Schema: public; Owner: aelaguiz; Tablespace: 
--

CREATE TABLE post_body (
    id bigint DEFAULT nextval('post_body_id'::regclass) NOT NULL,
    body character varying NOT NULL
);


ALTER TABLE public.post_body OWNER TO aelaguiz;

--
-- Name: post_hashtag_map; Type: TABLE; Schema: public; Owner: aelaguiz; Tablespace: 
--

CREATE TABLE post_hashtag_map (
    post_id bigint NOT NULL,
    hashtag_id bigint NOT NULL
);


ALTER TABLE public.post_hashtag_map OWNER TO aelaguiz;

--
-- Name: post_mention_map; Type: TABLE; Schema: public; Owner: aelaguiz; Tablespace: 
--

CREATE TABLE post_mention_map (
    post_id bigint NOT NULL,
    sn_id bigint NOT NULL
);


ALTER TABLE public.post_mention_map OWNER TO aelaguiz;

--
-- Name: post_url_map; Type: TABLE; Schema: public; Owner: aelaguiz; Tablespace: 
--

CREATE TABLE post_url_map (
    post_id bigint NOT NULL,
    url_id bigint NOT NULL
);


ALTER TABLE public.post_url_map OWNER TO aelaguiz;

--
-- Name: sn_id_seq; Type: SEQUENCE; Schema: public; Owner: aelaguiz
--

CREATE SEQUENCE sn_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sn_id_seq OWNER TO aelaguiz;

--
-- Name: sn; Type: TABLE; Schema: public; Owner: aelaguiz; Tablespace: 
--

CREATE TABLE sn (
    id bigint DEFAULT nextval('sn_id_seq'::regclass) NOT NULL,
    sn character varying NOT NULL,
    num_followers integer,
    num_friends integer,
    num_posts integer,
    verified boolean,
    num_favorites integer,
    last_check timestamp without time zone
);


ALTER TABLE public.sn OWNER TO aelaguiz;

--
-- Name: url_id_seq; Type: SEQUENCE; Schema: public; Owner: aelaguiz
--

CREATE SEQUENCE url_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.url_id_seq OWNER TO aelaguiz;

--
-- Name: url; Type: TABLE; Schema: public; Owner: aelaguiz; Tablespace: 
--

CREATE TABLE url (
    id bigint DEFAULT nextval('url_id_seq'::regclass) NOT NULL,
    url character varying NOT NULL
);


ALTER TABLE public.url OWNER TO aelaguiz;

--
-- Name: hashtag_pkey; Type: CONSTRAINT; Schema: public; Owner: aelaguiz; Tablespace: 
--

ALTER TABLE ONLY hashtag
    ADD CONSTRAINT hashtag_pkey PRIMARY KEY (id);


--
-- Name: post_body_pkey; Type: CONSTRAINT; Schema: public; Owner: aelaguiz; Tablespace: 
--

ALTER TABLE ONLY post_body
    ADD CONSTRAINT post_body_pkey PRIMARY KEY (id);


--
-- Name: sn_pkey; Type: CONSTRAINT; Schema: public; Owner: aelaguiz; Tablespace: 
--

ALTER TABLE ONLY sn
    ADD CONSTRAINT sn_pkey PRIMARY KEY (id);


--
-- Name: sn_unique_key; Type: CONSTRAINT; Schema: public; Owner: aelaguiz; Tablespace: 
--

ALTER TABLE ONLY sn
    ADD CONSTRAINT sn_unique_key UNIQUE (sn);


--
-- Name: tweet_hashtag_map_pkey; Type: CONSTRAINT; Schema: public; Owner: aelaguiz; Tablespace: 
--

ALTER TABLE ONLY post_hashtag_map
    ADD CONSTRAINT tweet_hashtag_map_pkey PRIMARY KEY (post_id, hashtag_id);


--
-- Name: tweet_mention_map_pkey; Type: CONSTRAINT; Schema: public; Owner: aelaguiz; Tablespace: 
--

ALTER TABLE ONLY post_mention_map
    ADD CONSTRAINT tweet_mention_map_pkey PRIMARY KEY (post_id, sn_id);


--
-- Name: tweet_pkey; Type: CONSTRAINT; Schema: public; Owner: aelaguiz; Tablespace: 
--

ALTER TABLE ONLY post
    ADD CONSTRAINT tweet_pkey PRIMARY KEY (id);


--
-- Name: tweet_url_map_pkey; Type: CONSTRAINT; Schema: public; Owner: aelaguiz; Tablespace: 
--

ALTER TABLE ONLY post_url_map
    ADD CONSTRAINT tweet_url_map_pkey PRIMARY KEY (post_id, url_id);


--
-- Name: url_pkey; Type: CONSTRAINT; Schema: public; Owner: aelaguiz; Tablespace: 
--

ALTER TABLE ONLY url
    ADD CONSTRAINT url_pkey PRIMARY KEY (id);


--
-- Name: post_body_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: aelaguiz
--

ALTER TABLE ONLY post
    ADD CONSTRAINT post_body_id_fkey FOREIGN KEY (body_id) REFERENCES post_body(id) ON DELETE CASCADE;


--
-- Name: tweet_hashtag_map_hashtag_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: aelaguiz
--

ALTER TABLE ONLY post_hashtag_map
    ADD CONSTRAINT tweet_hashtag_map_hashtag_id_fkey FOREIGN KEY (hashtag_id) REFERENCES hashtag(id) ON DELETE CASCADE;


--
-- Name: tweet_hashtag_map_tweet_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: aelaguiz
--

ALTER TABLE ONLY post_hashtag_map
    ADD CONSTRAINT tweet_hashtag_map_tweet_id_fkey FOREIGN KEY (post_id) REFERENCES post(id) ON DELETE CASCADE;


--
-- Name: tweet_mention_map_sn_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: aelaguiz
--

ALTER TABLE ONLY post_mention_map
    ADD CONSTRAINT tweet_mention_map_sn_id_fkey FOREIGN KEY (sn_id) REFERENCES sn(id) ON DELETE CASCADE;


--
-- Name: tweet_mention_map_tweet_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: aelaguiz
--

ALTER TABLE ONLY post_mention_map
    ADD CONSTRAINT tweet_mention_map_tweet_id_fkey FOREIGN KEY (post_id) REFERENCES post(id) ON DELETE CASCADE;


--
-- Name: tweet_sn_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: aelaguiz
--

ALTER TABLE ONLY post
    ADD CONSTRAINT tweet_sn_id_fkey FOREIGN KEY (sn_id) REFERENCES sn(id) ON DELETE CASCADE;


--
-- Name: tweet_url_map_tweet_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: aelaguiz
--

ALTER TABLE ONLY post_url_map
    ADD CONSTRAINT tweet_url_map_tweet_id_fkey FOREIGN KEY (post_id) REFERENCES post(id) ON DELETE CASCADE;


--
-- Name: tweet_url_map_url_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: aelaguiz
--

ALTER TABLE ONLY post_url_map
    ADD CONSTRAINT tweet_url_map_url_id_fkey FOREIGN KEY (url_id) REFERENCES url(id) ON DELETE CASCADE;


--
-- Name: public; Type: ACL; Schema: -; Owner: aelaguiz
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM aelaguiz;
GRANT ALL ON SCHEMA public TO aelaguiz;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

