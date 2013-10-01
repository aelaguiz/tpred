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

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: body_topic_map; Type: TABLE; Schema: public; Owner: aelaguiz; Tablespace: 
--

CREATE TABLE body_topic_map (
    body_id bigint NOT NULL,
    topic_id bigint NOT NULL
);


ALTER TABLE public.body_topic_map OWNER TO aelaguiz;

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
    site_post_id character varying NOT NULL,
    sn_id bigint NOT NULL,
    created_at timestamp without time zone NOT NULL,
    body_id bigint,
    site_id bigint,
    repost boolean DEFAULT false NOT NULL
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
    body text NOT NULL
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
-- Name: post_moment_id_seq; Type: SEQUENCE; Schema: public; Owner: aelaguiz
--

CREATE SEQUENCE post_moment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.post_moment_id_seq OWNER TO aelaguiz;

--
-- Name: post_moment; Type: TABLE; Schema: public; Owner: aelaguiz; Tablespace: 
--

CREATE TABLE post_moment (
    id bigint DEFAULT nextval('post_moment_id_seq'::regclass) NOT NULL,
    ts timestamp without time zone DEFAULT now() NOT NULL,
    points integer NOT NULL
);


ALTER TABLE public.post_moment OWNER TO aelaguiz;

--
-- Name: post_moment_map; Type: TABLE; Schema: public; Owner: aelaguiz; Tablespace: 
--

CREATE TABLE post_moment_map (
    post_id bigint NOT NULL,
    moment_id bigint NOT NULL
);


ALTER TABLE public.post_moment_map OWNER TO aelaguiz;

--
-- Name: post_url_map; Type: TABLE; Schema: public; Owner: aelaguiz; Tablespace: 
--

CREATE TABLE post_url_map (
    post_id bigint NOT NULL,
    url_id bigint NOT NULL
);


ALTER TABLE public.post_url_map OWNER TO aelaguiz;

--
-- Name: run_history; Type: TABLE; Schema: public; Owner: aelaguiz; Tablespace: 
--

CREATE TABLE run_history (
    key character varying NOT NULL,
    moment bigint NOT NULL
);


ALTER TABLE public.run_history OWNER TO aelaguiz;

--
-- Name: run_history_id_seq; Type: SEQUENCE; Schema: public; Owner: aelaguiz
--

CREATE SEQUENCE run_history_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.run_history_id_seq OWNER TO aelaguiz;

--
-- Name: site; Type: TABLE; Schema: public; Owner: aelaguiz; Tablespace: 
--

CREATE TABLE site (
    id bigint NOT NULL,
    site character varying NOT NULL
);


ALTER TABLE public.site OWNER TO aelaguiz;

--
-- Name: site_run_history; Type: TABLE; Schema: public; Owner: aelaguiz; Tablespace: 
--

CREATE TABLE site_run_history (
    site_id bigint NOT NULL,
    moment bigint NOT NULL
);


ALTER TABLE public.site_run_history OWNER TO aelaguiz;

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
    last_check timestamp without time zone,
    site_id bigint,
    site_sn_id bigint,
    deleted boolean DEFAULT false
);


ALTER TABLE public.sn OWNER TO aelaguiz;

--
-- Name: topic_id_seq; Type: SEQUENCE; Schema: public; Owner: aelaguiz
--

CREATE SEQUENCE topic_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.topic_id_seq OWNER TO aelaguiz;

--
-- Name: topic; Type: TABLE; Schema: public; Owner: aelaguiz; Tablespace: 
--

CREATE TABLE topic (
    id bigint DEFAULT nextval('topic_id_seq'::regclass) NOT NULL,
    topic character varying NOT NULL,
    num_words integer DEFAULT 1 NOT NULL,
    clustered boolean DEFAULT false
);


ALTER TABLE public.topic OWNER TO aelaguiz;

--
-- Name: topic_cluster_id; Type: SEQUENCE; Schema: public; Owner: aelaguiz
--

CREATE SEQUENCE topic_cluster_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.topic_cluster_id OWNER TO aelaguiz;

--
-- Name: topic_cluster; Type: TABLE; Schema: public; Owner: aelaguiz; Tablespace: 
--

CREATE TABLE topic_cluster (
    id bigint DEFAULT nextval('topic_cluster_id'::regclass) NOT NULL
);


ALTER TABLE public.topic_cluster OWNER TO aelaguiz;

--
-- Name: topic_cluster_map; Type: TABLE; Schema: public; Owner: aelaguiz; Tablespace: 
--

CREATE TABLE topic_cluster_map (
    cluster_id bigint NOT NULL,
    topic_id bigint NOT NULL
);


ALTER TABLE public.topic_cluster_map OWNER TO aelaguiz;

--
-- Name: topic_moment; Type: TABLE; Schema: public; Owner: aelaguiz; Tablespace: 
--

CREATE TABLE topic_moment (
    topic_id bigint NOT NULL,
    moment bigint NOT NULL,
    value bigint NOT NULL,
    site_id bigint NOT NULL
);


ALTER TABLE public.topic_moment OWNER TO aelaguiz;

--
-- Name: topic_moment_deriv_id_seq; Type: SEQUENCE; Schema: public; Owner: aelaguiz
--

CREATE SEQUENCE topic_moment_deriv_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.topic_moment_deriv_id_seq OWNER TO aelaguiz;

--
-- Name: topic_moment_deriv; Type: TABLE; Schema: public; Owner: aelaguiz; Tablespace: 
--

CREATE TABLE topic_moment_deriv (
    id bigint DEFAULT nextval('topic_moment_deriv_id_seq'::regclass) NOT NULL,
    site_id bigint NOT NULL,
    topic_id bigint NOT NULL,
    moment_from bigint NOT NULL,
    moment_to bigint NOT NULL,
    value double precision
);


ALTER TABLE public.topic_moment_deriv OWNER TO aelaguiz;

--
-- Name: topic_moment_id_seq; Type: SEQUENCE; Schema: public; Owner: aelaguiz
--

CREATE SEQUENCE topic_moment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.topic_moment_id_seq OWNER TO aelaguiz;

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
-- Name: body_topic_map_pkey; Type: CONSTRAINT; Schema: public; Owner: aelaguiz; Tablespace: 
--

ALTER TABLE ONLY body_topic_map
    ADD CONSTRAINT body_topic_map_pkey PRIMARY KEY (body_id, topic_id);


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
-- Name: post_moment_map_pkey; Type: CONSTRAINT; Schema: public; Owner: aelaguiz; Tablespace: 
--

ALTER TABLE ONLY post_moment_map
    ADD CONSTRAINT post_moment_map_pkey PRIMARY KEY (post_id, moment_id);


--
-- Name: post_moment_pkey; Type: CONSTRAINT; Schema: public; Owner: aelaguiz; Tablespace: 
--

ALTER TABLE ONLY post_moment
    ADD CONSTRAINT post_moment_pkey PRIMARY KEY (id);


--
-- Name: run_history_pkey; Type: CONSTRAINT; Schema: public; Owner: aelaguiz; Tablespace: 
--

ALTER TABLE ONLY run_history
    ADD CONSTRAINT run_history_pkey PRIMARY KEY (key, moment);


--
-- Name: site_pkey; Type: CONSTRAINT; Schema: public; Owner: aelaguiz; Tablespace: 
--

ALTER TABLE ONLY site
    ADD CONSTRAINT site_pkey PRIMARY KEY (id);


--
-- Name: site_run_history_pkey; Type: CONSTRAINT; Schema: public; Owner: aelaguiz; Tablespace: 
--

ALTER TABLE ONLY site_run_history
    ADD CONSTRAINT site_run_history_pkey PRIMARY KEY (site_id, moment);


--
-- Name: sn_pkey; Type: CONSTRAINT; Schema: public; Owner: aelaguiz; Tablespace: 
--

ALTER TABLE ONLY sn
    ADD CONSTRAINT sn_pkey PRIMARY KEY (id);


--
-- Name: sn_site_id_unique_key; Type: CONSTRAINT; Schema: public; Owner: aelaguiz; Tablespace: 
--

ALTER TABLE ONLY sn
    ADD CONSTRAINT sn_site_id_unique_key UNIQUE (site_id, sn);


--
-- Name: topic_cluster_map_pkey; Type: CONSTRAINT; Schema: public; Owner: aelaguiz; Tablespace: 
--

ALTER TABLE ONLY topic_cluster_map
    ADD CONSTRAINT topic_cluster_map_pkey PRIMARY KEY (cluster_id, topic_id);


--
-- Name: topic_cluster_pkey; Type: CONSTRAINT; Schema: public; Owner: aelaguiz; Tablespace: 
--

ALTER TABLE ONLY topic_cluster
    ADD CONSTRAINT topic_cluster_pkey PRIMARY KEY (id);


--
-- Name: topic_moment_deriv_pkey; Type: CONSTRAINT; Schema: public; Owner: aelaguiz; Tablespace: 
--

ALTER TABLE ONLY topic_moment_deriv
    ADD CONSTRAINT topic_moment_deriv_pkey PRIMARY KEY (id);


--
-- Name: topic_moment_pkey; Type: CONSTRAINT; Schema: public; Owner: aelaguiz; Tablespace: 
--

ALTER TABLE ONLY topic_moment
    ADD CONSTRAINT topic_moment_pkey PRIMARY KEY (topic_id, site_id, moment);


--
-- Name: topic_pkey; Type: CONSTRAINT; Schema: public; Owner: aelaguiz; Tablespace: 
--

ALTER TABLE ONLY topic
    ADD CONSTRAINT topic_pkey PRIMARY KEY (id);


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
-- Name: topic_moment_deriv_unique_index; Type: INDEX; Schema: public; Owner: aelaguiz; Tablespace: 
--

CREATE UNIQUE INDEX topic_moment_deriv_unique_index ON topic_moment_deriv USING btree (site_id, topic_id, moment_from, moment_to);


--
-- Name: body_topic_map_body_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: aelaguiz
--

ALTER TABLE ONLY body_topic_map
    ADD CONSTRAINT body_topic_map_body_id_fkey FOREIGN KEY (body_id) REFERENCES post_body(id) ON DELETE CASCADE;


--
-- Name: body_topic_map_topic_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: aelaguiz
--

ALTER TABLE ONLY body_topic_map
    ADD CONSTRAINT body_topic_map_topic_id_fkey FOREIGN KEY (topic_id) REFERENCES topic(id) ON DELETE CASCADE;


--
-- Name: post_body_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: aelaguiz
--

ALTER TABLE ONLY post
    ADD CONSTRAINT post_body_id_fkey FOREIGN KEY (body_id) REFERENCES post_body(id) ON DELETE CASCADE;


--
-- Name: post_moment_map_moment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: aelaguiz
--

ALTER TABLE ONLY post_moment_map
    ADD CONSTRAINT post_moment_map_moment_id_fkey FOREIGN KEY (moment_id) REFERENCES post_moment(id) ON DELETE CASCADE;


--
-- Name: post_moment_map_post_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: aelaguiz
--

ALTER TABLE ONLY post_moment_map
    ADD CONSTRAINT post_moment_map_post_id_fkey FOREIGN KEY (post_id) REFERENCES post(id) ON DELETE CASCADE;


--
-- Name: post_site_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: aelaguiz
--

ALTER TABLE ONLY post
    ADD CONSTRAINT post_site_id_fkey FOREIGN KEY (site_id) REFERENCES site(id);


--
-- Name: site_run_history_site_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: aelaguiz
--

ALTER TABLE ONLY site_run_history
    ADD CONSTRAINT site_run_history_site_id_fkey FOREIGN KEY (site_id) REFERENCES site(id);


--
-- Name: sn_site_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: aelaguiz
--

ALTER TABLE ONLY sn
    ADD CONSTRAINT sn_site_id_fkey FOREIGN KEY (site_id) REFERENCES site(id);


--
-- Name: topic_cluster_map_cluster_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: aelaguiz
--

ALTER TABLE ONLY topic_cluster_map
    ADD CONSTRAINT topic_cluster_map_cluster_id_fkey FOREIGN KEY (cluster_id) REFERENCES topic_cluster(id) ON DELETE CASCADE;


--
-- Name: topic_cluster_map_topic_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: aelaguiz
--

ALTER TABLE ONLY topic_cluster_map
    ADD CONSTRAINT topic_cluster_map_topic_id_fkey FOREIGN KEY (topic_id) REFERENCES topic(id) ON DELETE CASCADE;


--
-- Name: topic_moment_deriv_site_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: aelaguiz
--

ALTER TABLE ONLY topic_moment_deriv
    ADD CONSTRAINT topic_moment_deriv_site_id_fkey FOREIGN KEY (site_id) REFERENCES site(id) ON DELETE CASCADE;


--
-- Name: topic_moment_deriv_topic_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: aelaguiz
--

ALTER TABLE ONLY topic_moment_deriv
    ADD CONSTRAINT topic_moment_deriv_topic_id_fkey FOREIGN KEY (topic_id) REFERENCES topic(id) ON DELETE CASCADE;


--
-- Name: topic_moment_site_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: aelaguiz
--

ALTER TABLE ONLY topic_moment
    ADD CONSTRAINT topic_moment_site_id_fkey FOREIGN KEY (site_id) REFERENCES site(id) ON DELETE CASCADE;


--
-- Name: topic_moment_topic_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: aelaguiz
--

ALTER TABLE ONLY topic_moment
    ADD CONSTRAINT topic_moment_topic_id_fkey FOREIGN KEY (topic_id) REFERENCES topic(id) ON DELETE CASCADE;


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

