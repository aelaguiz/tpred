--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: moment_topic_post_count; Type: TABLE; Schema: public; Owner: aelaguiz; Tablespace: 
--

CREATE TABLE moment_topic_post_count (
    id bigint DEFAULT nextval('moment_topic_post_count_id_seq'::regclass) NOT NULL,
    topic_id bigint NOT NULL,
    body_id bigint NOT NULL,
    moment bigint NOT NULL,
    num_posts bigint NOT NULL
);


ALTER TABLE public.moment_topic_post_count OWNER TO aelaguiz;

--
-- Name: moment_topic_post_count_pkey; Type: CONSTRAINT; Schema: public; Owner: aelaguiz; Tablespace: 
--

ALTER TABLE ONLY moment_topic_post_count
    ADD CONSTRAINT moment_topic_post_count_pkey PRIMARY KEY (id);


--
-- Name: moment_topic_post_count_topic_id_body_id_moment_idx; Type: INDEX; Schema: public; Owner: aelaguiz; Tablespace: 
--

CREATE UNIQUE INDEX moment_topic_post_count_topic_id_body_id_moment_idx ON moment_topic_post_count USING btree (topic_id, body_id, moment);


--
-- Name: moment_topic_post_count_body_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: aelaguiz
--

ALTER TABLE ONLY moment_topic_post_count
    ADD CONSTRAINT moment_topic_post_count_body_id_fkey FOREIGN KEY (body_id) REFERENCES post_body(id);


--
-- Name: moment_topic_post_count_topic_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: aelaguiz
--

ALTER TABLE ONLY moment_topic_post_count
    ADD CONSTRAINT moment_topic_post_count_topic_id_fkey FOREIGN KEY (topic_id) REFERENCES topic(id);


--
-- PostgreSQL database dump complete
--

