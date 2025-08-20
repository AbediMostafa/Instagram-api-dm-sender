--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5
-- Dumped by pg_dump version 17.4 (Debian 17.4-1.pgdg120+2)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: command_type; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.command_type AS ENUM (
    'set name',
    'set username',
    'set bio',
    'set avatar',
    'post image',
    'post video',
    'post carousel',
    'follow',
    'dm follow up',
    'like post',
    'comment post',
    'custom message',
    'send loom',
    'loom follow up',
    'get threads',
    'delete initial posts',
    'get thread messages',
    'call booked',
    'make public',
    'number of active accounts',
    'follow good pages',
    'explore hashtag',
    'generate lead by followers',
    'generate lead by page engagement',
    'generate lead by post engagement'
);


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: account_template; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.account_template (
    id bigint NOT NULL,
    account_id bigint NOT NULL,
    template_id bigint NOT NULL
);


--
-- Name: account_template_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.account_template_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: account_template_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.account_template_id_seq OWNED BY public.account_template.id;


--
-- Name: accounts; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.accounts (
    id bigint NOT NULL,
    secret_key character varying(255),
    username character varying(255) NOT NULL,
    email character varying(255),
    password character varying(255) NOT NULL,
    name character varying(255),
    bio text,
    profile_pic_url text,
    instagram_state character varying(255) DEFAULT 'active'::character varying NOT NULL,
    app_state character varying(255) DEFAULT 'idle'::character varying NOT NULL,
    color_id bigint,
    category_id bigint,
    proxy_id bigint,
    profile_id bigint,
    is_used smallint DEFAULT '0'::smallint NOT NULL,
    avatar_changed smallint DEFAULT '0'::smallint NOT NULL,
    username_changed smallint DEFAULT '0'::smallint NOT NULL,
    initial_posts_deleted smallint DEFAULT '0'::smallint NOT NULL,
    has_enough_posts smallint DEFAULT '0'::smallint NOT NULL,
    is_public smallint DEFAULT '0'::smallint NOT NULL,
    is_active smallint DEFAULT '1'::smallint NOT NULL,
    web_session text,
    mobile_session text,
    log text,
    created_at timestamp(0) without time zone,
    updated_at timestamp(0) without time zone,
    next_login timestamp(0) without time zone,
    fingerprint jsonb,
    phone character varying,
    screenshot_taken smallint DEFAULT 0 NOT NULL,
    CONSTRAINT accounts_app_state_check CHECK (((app_state)::text = ANY (ARRAY[('idle'::character varying)::text, ('processing'::character varying)::text, ('set name'::character varying)::text, ('set username'::character varying)::text, ('set bio'::character varying)::text, ('set avatar'::character varying)::text, ('post image'::character varying)::text, ('post carousel'::character varying)::text, ('post video'::character varying)::text, ('following'::character varying)::text, ('sending DM'::character varying)::text, ('make public'::character varying)::text, ('loom follow up'::character varying)::text, ('delete initial posts'::character varying)::text, ('get thread messages'::character varying)::text]))),
    CONSTRAINT accounts_instagram_state_check CHECK (((instagram_state)::text = ANY (ARRAY[('active'::character varying)::text, ('challenging'::character varying)::text, ('follow ban'::character varying)::text, ('login required'::character varying)::text, ('action ban'::character varying)::text, ('bad password'::character varying)::text, ('proxy blocked'::character varying)::text, ('wait a few minutes'::character varying)::text, ('two factor required'::character varying)::text, ('doesnt followed dm limit'::character varying)::text, ('suspended'::character varying)::text])))
);


--
-- Name: accounts_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.accounts_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: accounts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.accounts_id_seq OWNED BY public.accounts.id;


--
-- Name: ads_power_locks; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ads_power_locks (
    last_executed_at timestamp(0) without time zone NOT NULL,
    id integer NOT NULL
);


--
-- Name: ads_power_locks_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ads_power_locks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ads_power_locks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ads_power_locks_id_seq OWNED BY public.ads_power_locks.id;


--
-- Name: cache; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cache (
    key character varying(255) NOT NULL,
    value text NOT NULL,
    expiration integer NOT NULL
);


--
-- Name: cache_locks; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cache_locks (
    key character varying(255) NOT NULL,
    owner character varying(255) NOT NULL,
    expiration integer NOT NULL
);


--
-- Name: categories; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.categories (
    id bigint NOT NULL,
    title character varying(255) NOT NULL,
    number_of_follow_ups integer NOT NULL,
    hour_interval integer DEFAULT 24 NOT NULL,
    description text,
    created_at timestamp(0) without time zone,
    updated_at timestamp(0) without time zone
);


--
-- Name: categories_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.categories_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.categories_id_seq OWNED BY public.categories.id;


--
-- Name: clis; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.clis (
    id bigint NOT NULL,
    account_id bigint NOT NULL,
    process_id bigint,
    log character varying(255) NOT NULL,
    created_at timestamp(0) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


--
-- Name: clis_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.clis_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: clis_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.clis_id_seq OWNED BY public.clis.id;


--
-- Name: colors; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.colors (
    id bigint NOT NULL,
    title character varying(255) NOT NULL,
    is_used smallint DEFAULT '0'::smallint NOT NULL
);


--
-- Name: colors_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.colors_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: colors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.colors_id_seq OWNED BY public.colors.id;


--
-- Name: commands; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.commands (
    id bigint NOT NULL,
    account_id bigint,
    lead_id bigint,
    parent_command_id bigint,
    category_id bigint,
    commandable_id integer,
    commandable_type character varying(255),
    times integer DEFAULT 0 NOT NULL,
    type character varying(255) NOT NULL,
    state character varying(255) NOT NULL,
    created_at timestamp(0) without time zone,
    updated_at timestamp(0) without time zone,
    CONSTRAINT commands_state_check CHECK (((state)::text = ANY (ARRAY[('pending'::character varying)::text, ('processing'::character varying)::text, ('success'::character varying)::text, ('fail'::character varying)::text])))
);


--
-- Name: commands_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.commands_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: commands_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.commands_id_seq OWNED BY public.commands.id;


--
-- Name: dm_post_lead; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.dm_post_lead (
    id bigint NOT NULL,
    lead_id bigint NOT NULL,
    dm_post_id bigint NOT NULL
);


--
-- Name: dm_post_lead_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.dm_post_lead_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: dm_post_lead_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.dm_post_lead_id_seq OWNED BY public.dm_post_lead.id;


--
-- Name: dm_posts; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.dm_posts (
    id bigint NOT NULL,
    title character varying(255) NOT NULL,
    description text,
    category_id bigint,
    created_at timestamp(0) without time zone DEFAULT CURRENT_TIMESTAMP,
    priority smallint DEFAULT 0,
    media_id character varying(255)
);


--
-- Name: dm_posts_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.dm_posts_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: dm_posts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.dm_posts_id_seq OWNED BY public.dm_posts.id;


--
-- Name: hashtags; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.hashtags (
    id bigint NOT NULL,
    title character varying(255) NOT NULL,
    is_used smallint DEFAULT '0'::smallint NOT NULL,
    category_id bigint,
    created_at timestamp(0) without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: hashtags_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.hashtags_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: hashtags_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.hashtags_id_seq OWNED BY public.hashtags.id;


--
-- Name: lead_histories; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.lead_histories (
    id bigint NOT NULL,
    state character varying(255) DEFAULT 'free'::character varying NOT NULL,
    times integer DEFAULT 0,
    lead_id bigint NOT NULL,
    account_id bigint,
    user_id bigint,
    created_at timestamp(0) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT lead_histories_state_check CHECK (((state)::text = ANY (ARRAY[('free'::character varying)::text, ('followed'::character varying)::text, ('dm follow up'::character varying)::text, ('unseen dm reply'::character varying)::text, ('seen dm reply'::character varying)::text, ('needs response'::character varying)::text, ('interested'::character varying)::text, ('not interested'::character varying)::text, ('loom follow up'::character varying)::text, ('unseen loom reply'::character varying)::text, ('seen loom reply'::character varying)::text, ('failed dm'::character varying)::text, ('failed loom dm'::character varying)::text, ('call booked'::character varying)::text])))
);


--
-- Name: lead_histories_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.lead_histories_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: lead_histories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.lead_histories_id_seq OWNED BY public.lead_histories.id;


--
-- Name: lead_sources; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.lead_sources (
    id bigint NOT NULL,
    title character varying(255) NOT NULL,
    is_used smallint DEFAULT '0'::smallint NOT NULL,
    category_id bigint,
    created_at timestamp(0) without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: lead_sources_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.lead_sources_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: lead_sources_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.lead_sources_id_seq OWNED BY public.lead_sources.id;


--
-- Name: leads; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.leads (
    id bigint NOT NULL,
    instagram_id bigint,
    username character varying(255) NOT NULL,
    times integer DEFAULT 0,
    last_state character varying(255) DEFAULT 'free'::character varying NOT NULL,
    account_id bigint,
    user_id bigint,
    category_id bigint,
    export_date timestamp(0) without time zone,
    last_command_send_date timestamp(0) without time zone,
    created_at timestamp(0) without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT leads_last_state_check CHECK (((last_state)::text = ANY (ARRAY[('free'::character varying)::text, ('followed'::character varying)::text, ('dm follow up'::character varying)::text, ('unseen dm reply'::character varying)::text, ('seen dm reply'::character varying)::text, ('needs response'::character varying)::text, ('interested'::character varying)::text, ('not interested'::character varying)::text, ('loom follow up'::character varying)::text, ('unseen loom reply'::character varying)::text, ('seen loom reply'::character varying)::text, ('failed dm'::character varying)::text, ('failed loom dm'::character varying)::text, ('call booked'::character varying)::text])))
);


--
-- Name: COLUMN leads.export_date; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.leads.export_date IS 'Date we pull lead';


--
-- Name: leads_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.leads_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: leads_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.leads_id_seq OWNED BY public.leads.id;


--
-- Name: logs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.logs (
    id bigint NOT NULL,
    account_id bigint NOT NULL,
    log text NOT NULL,
    created_at timestamp(0) without time zone NOT NULL
);


--
-- Name: logs_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.logs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: logs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.logs_id_seq OWNED BY public.logs.id;


--
-- Name: looms; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.looms (
    id bigint NOT NULL,
    hashed_name character varying(255) NOT NULL,
    original_name character varying(255) NOT NULL,
    path character varying(255) NOT NULL,
    description text,
    state character varying(255) DEFAULT 'pending'::character varying NOT NULL,
    account_id bigint,
    lead_id bigint,
    created_at timestamp(0) without time zone,
    updated_at timestamp(0) without time zone,
    CONSTRAINT looms_state_check CHECK (((state)::text = ANY (ARRAY[('uploaded'::character varying)::text, ('pending'::character varying)::text, ('sent'::character varying)::text])))
);


--
-- Name: looms_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.looms_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: looms_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.looms_id_seq OWNED BY public.looms.id;


--
-- Name: messages; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.messages (
    id bigint NOT NULL,
    message_id character varying(255),
    thread_id bigint,
    messageable_id bigint,
    messageable_type character varying(255),
    text text,
    sender character varying(255) DEFAULT 'account'::character varying NOT NULL,
    type character varying(255) DEFAULT 'text'::character varying NOT NULL,
    state character varying(255) DEFAULT 'seen'::character varying NOT NULL,
    created_at timestamp(0) without time zone NOT NULL,
    CONSTRAINT messages_sender_check CHECK (((sender)::text = ANY (ARRAY[('account'::character varying)::text, ('lead'::character varying)::text]))),
    CONSTRAINT messages_state_check CHECK (((state)::text = ANY (ARRAY[('fail'::character varying)::text, ('seen'::character varying)::text, ('unseen'::character varying)::text, ('pending'::character varying)::text]))),
    CONSTRAINT messages_type_check CHECK (((type)::text = ANY (ARRAY[('text'::character varying)::text, ('post'::character varying)::text, ('loom'::character varying)::text])))
);


--
-- Name: messages_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.messages_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: messages_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.messages_id_seq OWNED BY public.messages.id;


--
-- Name: migrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.migrations (
    id integer NOT NULL,
    migration character varying(255) NOT NULL,
    batch integer NOT NULL
);


--
-- Name: migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.migrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.migrations_id_seq OWNED BY public.migrations.id;


--
-- Name: notifs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.notifs (
    id bigint NOT NULL,
    account_id bigint NOT NULL,
    lead_id bigint NOT NULL,
    thread_id bigint NOT NULL,
    message_id bigint NOT NULL,
    visibility character varying(255) DEFAULT 'unseen'::character varying NOT NULL,
    created_at timestamp(0) without time zone NOT NULL,
    CONSTRAINT notifs_visibility_check CHECK (((visibility)::text = ANY (ARRAY[('seen'::character varying)::text, ('unseen'::character varying)::text])))
);


--
-- Name: notifs_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.notifs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: notifs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.notifs_id_seq OWNED BY public.notifs.id;


--
-- Name: permission_role; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.permission_role (
    permission_id bigint NOT NULL,
    role_id bigint NOT NULL
);


--
-- Name: permission_user; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.permission_user (
    permission_id bigint NOT NULL,
    user_id bigint NOT NULL,
    user_type character varying(255) NOT NULL
);


--
-- Name: permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.permissions (
    id bigint NOT NULL,
    name character varying(255) NOT NULL,
    display_name character varying(255),
    description character varying(255),
    created_at timestamp(0) without time zone,
    updated_at timestamp(0) without time zone
);


--
-- Name: permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.permissions_id_seq OWNED BY public.permissions.id;


--
-- Name: personal_access_tokens; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.personal_access_tokens (
    id bigint NOT NULL,
    tokenable_type character varying(255) NOT NULL,
    tokenable_id bigint NOT NULL,
    name character varying(255) NOT NULL,
    token character varying(64) NOT NULL,
    abilities text,
    last_used_at timestamp(0) without time zone,
    expires_at timestamp(0) without time zone,
    created_at timestamp(0) without time zone,
    updated_at timestamp(0) without time zone
);


--
-- Name: personal_access_tokens_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.personal_access_tokens_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: personal_access_tokens_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.personal_access_tokens_id_seq OWNED BY public.personal_access_tokens.id;


--
-- Name: processes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.processes (
    id bigint NOT NULL,
    pid bigint NOT NULL,
    status character varying(255) DEFAULT 'running'::character varying NOT NULL,
    created_at timestamp(0) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT processes_status_check CHECK (((status)::text = ANY (ARRAY[('running'::character varying)::text, ('stopped'::character varying)::text, ('terminated'::character varying)::text])))
);


--
-- Name: processes_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.processes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: processes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.processes_id_seq OWNED BY public.processes.id;


--
-- Name: profiles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.profiles (
    id bigint NOT NULL,
    title character varying(255) NOT NULL,
    folder character varying(255) NOT NULL,
    profile_id character varying(255) NOT NULL,
    proxy_id bigint,
    created_at timestamp(0) without time zone,
    updated_at timestamp(0) without time zone,
    is_used smallint DEFAULT 0 NOT NULL
);


--
-- Name: profiles_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.profiles_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: profiles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.profiles_id_seq OWNED BY public.profiles.id;


--
-- Name: proxies; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.proxies (
    id bigint NOT NULL,
    ip character varying(255) NOT NULL,
    port integer NOT NULL,
    username character varying(255) NOT NULL,
    password character varying(255) NOT NULL,
    state character varying(255) DEFAULT 'active'::character varying NOT NULL,
    is_used smallint DEFAULT 0 NOT NULL,
    CONSTRAINT proxies_state_check CHECK (((state)::text = ANY (ARRAY[('active'::character varying)::text, ('inactive'::character varying)::text])))
);


--
-- Name: proxies_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.proxies_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: proxies_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.proxies_id_seq OWNED BY public.proxies.id;


--
-- Name: role_user; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.role_user (
    role_id bigint NOT NULL,
    user_id bigint NOT NULL,
    user_type character varying(255) NOT NULL
);


--
-- Name: roles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.roles (
    id bigint NOT NULL,
    name character varying(255) NOT NULL,
    display_name character varying(255),
    description character varying(255),
    created_at timestamp(0) without time zone,
    updated_at timestamp(0) without time zone
);


--
-- Name: roles_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.roles_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.roles_id_seq OWNED BY public.roles.id;


--
-- Name: screen_resolutions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.screen_resolutions (
    id bigint NOT NULL,
    width integer NOT NULL,
    height integer NOT NULL,
    is_used smallint DEFAULT '0'::smallint NOT NULL
);


--
-- Name: screen_resolutions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.screen_resolutions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: screen_resolutions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.screen_resolutions_id_seq OWNED BY public.screen_resolutions.id;


--
-- Name: screen_shots; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.screen_shots (
    id bigint NOT NULL,
    cause character varying(255) NOT NULL,
    path character varying(255) NOT NULL,
    account_id bigint NOT NULL,
    created_at timestamp(0) without time zone NOT NULL
);


--
-- Name: screen_shots_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.screen_shots_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: screen_shots_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.screen_shots_id_seq OWNED BY public.screen_shots.id;


--
-- Name: sessions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sessions (
    id character varying(255) NOT NULL,
    user_id bigint,
    ip_address character varying(45),
    user_agent text,
    payload text NOT NULL,
    last_activity integer NOT NULL
);


--
-- Name: settings; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.settings (
    id bigint NOT NULL,
    type character varying(255) DEFAULT 'text'::character varying NOT NULL,
    category character varying(255),
    key character varying(255) NOT NULL,
    value text NOT NULL,
    description character varying(255),
    CONSTRAINT settings_category_check CHECK (((category)::text = ANY (ARRAY[('Follow'::character varying)::text, ('DM'::character varying)::text, ('Templates'::character varying)::text, ('Proxy'::character varying)::text, ('Command'::character varying)::text, ('Comment'::character varying)::text, ('Like'::character varying)::text]))),
    CONSTRAINT settings_type_check CHECK (((type)::text = ANY (ARRAY[('number'::character varying)::text, ('text'::character varying)::text, ('switch'::character varying)::text])))
);


--
-- Name: settings_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.settings_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: settings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.settings_id_seq OWNED BY public.settings.id;


--
-- Name: spintaxes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.spintaxes (
    id bigint NOT NULL,
    name character varying(255) NOT NULL,
    times integer DEFAULT 0 NOT NULL,
    text text NOT NULL,
    category_id bigint,
    created_at timestamp(0) without time zone,
    updated_at timestamp(0) without time zone
);


--
-- Name: spintaxes_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.spintaxes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: spintaxes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.spintaxes_id_seq OWNED BY public.spintaxes.id;


--
-- Name: taggables; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.taggables (
    tag_id bigint NOT NULL,
    taggable_id integer NOT NULL,
    taggable_type character varying(255) NOT NULL
);


--
-- Name: tags; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tags (
    id bigint NOT NULL,
    title character varying(255) NOT NULL,
    created_at timestamp(0) without time zone NOT NULL
);


--
-- Name: tags_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tags_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tags_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tags_id_seq OWNED BY public.tags.id;


--
-- Name: templates; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.templates (
    id bigint NOT NULL,
    text text NOT NULL,
    caption text,
    carousel_id character varying(255),
    uid character varying(255),
    color_id bigint,
    category_id bigint,
    type character varying(255) NOT NULL,
    sub_type character varying(255),
    created_at timestamp(0) without time zone,
    CONSTRAINT templates_sub_type_check CHECK (((sub_type)::text = ANY (ARRAY[('image'::character varying)::text, ('video'::character varying)::text]))),
    CONSTRAINT templates_type_check CHECK (((type)::text = ANY (ARRAY[('name'::character varying)::text, ('username'::character varying)::text, ('bio'::character varying)::text, ('avatar'::character varying)::text, ('carousel'::character varying)::text, ('image-post'::character varying)::text, ('video-post'::character varying)::text])))
);


--
-- Name: templates_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.templates_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: templates_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.templates_id_seq OWNED BY public.templates.id;


--
-- Name: threads; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.threads (
    id bigint NOT NULL,
    thread_id character varying(255),
    thread_url_id character varying(255),
    account_id bigint,
    lead_id bigint,
    category_id bigint,
    created_at timestamp(0) without time zone NOT NULL
);


--
-- Name: threads_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.threads_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: threads_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.threads_id_seq OWNED BY public.threads.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id bigint NOT NULL,
    name character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    password character varying(255) NOT NULL,
    created_at timestamp(0) without time zone,
    updated_at timestamp(0) without time zone
);


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: warnings; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.warnings (
    id bigint NOT NULL,
    cause text,
    duration integer DEFAULT 24 NOT NULL,
    account_id bigint NOT NULL,
    created_at timestamp(0) without time zone NOT NULL
);


--
-- Name: warnings_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.warnings_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: warnings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.warnings_id_seq OWNED BY public.warnings.id;


--
-- Name: account_template id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.account_template ALTER COLUMN id SET DEFAULT nextval('public.account_template_id_seq'::regclass);


--
-- Name: accounts id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.accounts ALTER COLUMN id SET DEFAULT nextval('public.accounts_id_seq'::regclass);


--
-- Name: ads_power_locks id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ads_power_locks ALTER COLUMN id SET DEFAULT nextval('public.ads_power_locks_id_seq'::regclass);


--
-- Name: categories id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.categories ALTER COLUMN id SET DEFAULT nextval('public.categories_id_seq'::regclass);


--
-- Name: clis id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.clis ALTER COLUMN id SET DEFAULT nextval('public.clis_id_seq'::regclass);


--
-- Name: colors id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.colors ALTER COLUMN id SET DEFAULT nextval('public.colors_id_seq'::regclass);


--
-- Name: commands id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.commands ALTER COLUMN id SET DEFAULT nextval('public.commands_id_seq'::regclass);


--
-- Name: dm_post_lead id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dm_post_lead ALTER COLUMN id SET DEFAULT nextval('public.dm_post_lead_id_seq'::regclass);


--
-- Name: dm_posts id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dm_posts ALTER COLUMN id SET DEFAULT nextval('public.dm_posts_id_seq'::regclass);


--
-- Name: hashtags id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hashtags ALTER COLUMN id SET DEFAULT nextval('public.hashtags_id_seq'::regclass);


--
-- Name: lead_histories id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lead_histories ALTER COLUMN id SET DEFAULT nextval('public.lead_histories_id_seq'::regclass);


--
-- Name: lead_sources id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lead_sources ALTER COLUMN id SET DEFAULT nextval('public.lead_sources_id_seq'::regclass);


--
-- Name: leads id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.leads ALTER COLUMN id SET DEFAULT nextval('public.leads_id_seq'::regclass);


--
-- Name: logs id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.logs ALTER COLUMN id SET DEFAULT nextval('public.logs_id_seq'::regclass);


--
-- Name: looms id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.looms ALTER COLUMN id SET DEFAULT nextval('public.looms_id_seq'::regclass);


--
-- Name: messages id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.messages ALTER COLUMN id SET DEFAULT nextval('public.messages_id_seq'::regclass);


--
-- Name: migrations id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.migrations ALTER COLUMN id SET DEFAULT nextval('public.migrations_id_seq'::regclass);


--
-- Name: notifs id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notifs ALTER COLUMN id SET DEFAULT nextval('public.notifs_id_seq'::regclass);


--
-- Name: permissions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.permissions ALTER COLUMN id SET DEFAULT nextval('public.permissions_id_seq'::regclass);


--
-- Name: personal_access_tokens id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.personal_access_tokens ALTER COLUMN id SET DEFAULT nextval('public.personal_access_tokens_id_seq'::regclass);


--
-- Name: processes id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.processes ALTER COLUMN id SET DEFAULT nextval('public.processes_id_seq'::regclass);


--
-- Name: profiles id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.profiles ALTER COLUMN id SET DEFAULT nextval('public.profiles_id_seq'::regclass);


--
-- Name: proxies id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.proxies ALTER COLUMN id SET DEFAULT nextval('public.proxies_id_seq'::regclass);


--
-- Name: roles id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles ALTER COLUMN id SET DEFAULT nextval('public.roles_id_seq'::regclass);


--
-- Name: screen_resolutions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.screen_resolutions ALTER COLUMN id SET DEFAULT nextval('public.screen_resolutions_id_seq'::regclass);


--
-- Name: screen_shots id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.screen_shots ALTER COLUMN id SET DEFAULT nextval('public.screen_shots_id_seq'::regclass);


--
-- Name: settings id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.settings ALTER COLUMN id SET DEFAULT nextval('public.settings_id_seq'::regclass);


--
-- Name: spintaxes id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.spintaxes ALTER COLUMN id SET DEFAULT nextval('public.spintaxes_id_seq'::regclass);


--
-- Name: tags id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tags ALTER COLUMN id SET DEFAULT nextval('public.tags_id_seq'::regclass);


--
-- Name: templates id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.templates ALTER COLUMN id SET DEFAULT nextval('public.templates_id_seq'::regclass);


--
-- Name: threads id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.threads ALTER COLUMN id SET DEFAULT nextval('public.threads_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: warnings id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.warnings ALTER COLUMN id SET DEFAULT nextval('public.warnings_id_seq'::regclass);


--
-- Name: account_template account_template_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.account_template
    ADD CONSTRAINT account_template_pkey PRIMARY KEY (id);


--
-- Name: accounts accounts_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT accounts_pkey PRIMARY KEY (id);


--
-- Name: accounts accounts_username_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT accounts_username_unique UNIQUE (username);


--
-- Name: ads_power_locks ads_power_locks_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ads_power_locks
    ADD CONSTRAINT ads_power_locks_pkey PRIMARY KEY (id);


--
-- Name: cache_locks cache_locks_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cache_locks
    ADD CONSTRAINT cache_locks_pkey PRIMARY KEY (key);


--
-- Name: cache cache_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cache
    ADD CONSTRAINT cache_pkey PRIMARY KEY (key);


--
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);


--
-- Name: clis clis_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.clis
    ADD CONSTRAINT clis_pkey PRIMARY KEY (id);


--
-- Name: colors colors_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.colors
    ADD CONSTRAINT colors_pkey PRIMARY KEY (id);


--
-- Name: colors colors_title_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.colors
    ADD CONSTRAINT colors_title_unique UNIQUE (title);


--
-- Name: commands commands_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.commands
    ADD CONSTRAINT commands_pkey PRIMARY KEY (id);


--
-- Name: dm_post_lead dm_post_lead_dm_post_id_lead_id_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dm_post_lead
    ADD CONSTRAINT dm_post_lead_dm_post_id_lead_id_unique UNIQUE (dm_post_id, lead_id);


--
-- Name: dm_post_lead dm_post_lead_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dm_post_lead
    ADD CONSTRAINT dm_post_lead_pkey PRIMARY KEY (id);


--
-- Name: dm_posts dm_posts_media_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dm_posts
    ADD CONSTRAINT dm_posts_media_id_key UNIQUE (media_id);


--
-- Name: dm_posts dm_posts_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dm_posts
    ADD CONSTRAINT dm_posts_pkey PRIMARY KEY (id);


--
-- Name: hashtags hashtags_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hashtags
    ADD CONSTRAINT hashtags_pkey PRIMARY KEY (id);


--
-- Name: hashtags hashtags_title_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hashtags
    ADD CONSTRAINT hashtags_title_unique UNIQUE (title);


--
-- Name: lead_histories lead_histories_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lead_histories
    ADD CONSTRAINT lead_histories_pkey PRIMARY KEY (id);


--
-- Name: lead_sources lead_sources_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lead_sources
    ADD CONSTRAINT lead_sources_pkey PRIMARY KEY (id);


--
-- Name: lead_sources lead_sources_title_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lead_sources
    ADD CONSTRAINT lead_sources_title_unique UNIQUE (title);


--
-- Name: leads leads_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.leads
    ADD CONSTRAINT leads_pkey PRIMARY KEY (id);


--
-- Name: leads leads_username_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.leads
    ADD CONSTRAINT leads_username_unique UNIQUE (username);


--
-- Name: logs logs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.logs
    ADD CONSTRAINT logs_pkey PRIMARY KEY (id);


--
-- Name: looms looms_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.looms
    ADD CONSTRAINT looms_pkey PRIMARY KEY (id);


--
-- Name: messages messages_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_pkey PRIMARY KEY (id);


--
-- Name: migrations migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.migrations
    ADD CONSTRAINT migrations_pkey PRIMARY KEY (id);


--
-- Name: notifs notifs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notifs
    ADD CONSTRAINT notifs_pkey PRIMARY KEY (id);


--
-- Name: permission_role permission_role_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.permission_role
    ADD CONSTRAINT permission_role_pkey PRIMARY KEY (permission_id, role_id);


--
-- Name: permission_user permission_user_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.permission_user
    ADD CONSTRAINT permission_user_pkey PRIMARY KEY (user_id, permission_id, user_type);


--
-- Name: permissions permissions_name_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT permissions_name_unique UNIQUE (name);


--
-- Name: permissions permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT permissions_pkey PRIMARY KEY (id);


--
-- Name: personal_access_tokens personal_access_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.personal_access_tokens
    ADD CONSTRAINT personal_access_tokens_pkey PRIMARY KEY (id);


--
-- Name: personal_access_tokens personal_access_tokens_token_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.personal_access_tokens
    ADD CONSTRAINT personal_access_tokens_token_unique UNIQUE (token);


--
-- Name: processes processes_pid_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.processes
    ADD CONSTRAINT processes_pid_unique UNIQUE (pid);


--
-- Name: processes processes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.processes
    ADD CONSTRAINT processes_pkey PRIMARY KEY (id);


--
-- Name: profiles profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.profiles
    ADD CONSTRAINT profiles_pkey PRIMARY KEY (id);


--
-- Name: proxies proxies_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.proxies
    ADD CONSTRAINT proxies_pkey PRIMARY KEY (id);


--
-- Name: role_user role_user_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.role_user
    ADD CONSTRAINT role_user_pkey PRIMARY KEY (user_id, role_id, user_type);


--
-- Name: roles roles_name_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_name_unique UNIQUE (name);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- Name: screen_resolutions screen_resolutions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.screen_resolutions
    ADD CONSTRAINT screen_resolutions_pkey PRIMARY KEY (id);


--
-- Name: screen_shots screen_shots_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.screen_shots
    ADD CONSTRAINT screen_shots_pkey PRIMARY KEY (id);


--
-- Name: sessions sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sessions
    ADD CONSTRAINT sessions_pkey PRIMARY KEY (id);


--
-- Name: settings settings_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.settings
    ADD CONSTRAINT settings_pkey PRIMARY KEY (id);


--
-- Name: spintaxes spintaxes_name_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.spintaxes
    ADD CONSTRAINT spintaxes_name_unique UNIQUE (name);


--
-- Name: spintaxes spintaxes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.spintaxes
    ADD CONSTRAINT spintaxes_pkey PRIMARY KEY (id);


--
-- Name: tags tags_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tags
    ADD CONSTRAINT tags_pkey PRIMARY KEY (id);


--
-- Name: tags tags_title_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tags
    ADD CONSTRAINT tags_title_unique UNIQUE (title);


--
-- Name: templates templates_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.templates
    ADD CONSTRAINT templates_pkey PRIMARY KEY (id);


--
-- Name: threads threads_account_id_lead_id_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.threads
    ADD CONSTRAINT threads_account_id_lead_id_unique UNIQUE (account_id, lead_id);


--
-- Name: threads threads_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.threads
    ADD CONSTRAINT threads_pkey PRIMARY KEY (id);


--
-- Name: users users_email_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_unique UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: warnings warnings_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.warnings
    ADD CONSTRAINT warnings_pkey PRIMARY KEY (id);


--
-- Name: idx_accounts_category_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_accounts_category_id ON public.accounts USING btree (category_id);


--
-- Name: idx_accounts_created_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_accounts_created_at ON public.accounts USING btree (created_at);


--
-- Name: idx_accounts_instagram_state; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_accounts_instagram_state ON public.accounts USING btree (instagram_state);


--
-- Name: idx_accounts_profile_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_accounts_profile_id ON public.accounts USING btree (profile_id);


--
-- Name: idx_accounts_proxy_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_accounts_proxy_id ON public.accounts USING btree (proxy_id);


--
-- Name: idx_accounts_username; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_accounts_username ON public.accounts USING btree (username);


--
-- Name: idx_commands_account_id_type_state_times_created; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_commands_account_id_type_state_times_created ON public.commands USING btree (account_id, type, state, times, created_at);


--
-- Name: idx_messages_thread_id_sender_type_created; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_messages_thread_id_sender_type_created ON public.messages USING btree (thread_id, sender, type, created_at);


--
-- Name: idx_tag_taggable; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_tag_taggable ON public.taggables USING btree (taggable_id);


--
-- Name: idx_taggable_tag; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_taggable_tag ON public.taggables USING btree (tag_id);


--
-- Name: idx_warnings_account_id_created; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_warnings_account_id_created ON public.warnings USING btree (account_id, created_at DESC);


--
-- Name: personal_access_tokens_tokenable_type_tokenable_id_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX personal_access_tokens_tokenable_type_tokenable_id_index ON public.personal_access_tokens USING btree (tokenable_type, tokenable_id);


--
-- Name: sessions_last_activity_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX sessions_last_activity_index ON public.sessions USING btree (last_activity);


--
-- Name: sessions_user_id_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX sessions_user_id_index ON public.sessions USING btree (user_id);


--
-- Name: account_template account_template_account_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.account_template
    ADD CONSTRAINT account_template_account_id_foreign FOREIGN KEY (account_id) REFERENCES public.accounts(id) ON DELETE CASCADE;


--
-- Name: account_template account_template_template_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.account_template
    ADD CONSTRAINT account_template_template_id_foreign FOREIGN KEY (template_id) REFERENCES public.templates(id) ON DELETE CASCADE;


--
-- Name: accounts accounts_category_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT accounts_category_id_foreign FOREIGN KEY (category_id) REFERENCES public.categories(id) ON DELETE SET NULL;


--
-- Name: accounts accounts_color_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT accounts_color_id_foreign FOREIGN KEY (color_id) REFERENCES public.colors(id) ON DELETE SET NULL;


--
-- Name: accounts accounts_profile_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT accounts_profile_id_foreign FOREIGN KEY (profile_id) REFERENCES public.profiles(id) ON DELETE SET NULL;


--
-- Name: accounts accounts_proxy_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT accounts_proxy_id_foreign FOREIGN KEY (proxy_id) REFERENCES public.proxies(id) ON DELETE SET NULL;


--
-- Name: clis clis_account_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.clis
    ADD CONSTRAINT clis_account_id_foreign FOREIGN KEY (account_id) REFERENCES public.accounts(id) ON DELETE CASCADE;


--
-- Name: clis clis_process_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.clis
    ADD CONSTRAINT clis_process_id_foreign FOREIGN KEY (process_id) REFERENCES public.processes(id) ON DELETE SET NULL;


--
-- Name: commands commands_account_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.commands
    ADD CONSTRAINT commands_account_id_foreign FOREIGN KEY (account_id) REFERENCES public.accounts(id) ON DELETE CASCADE;


--
-- Name: commands commands_category_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.commands
    ADD CONSTRAINT commands_category_id_foreign FOREIGN KEY (category_id) REFERENCES public.categories(id) ON DELETE SET NULL;


--
-- Name: commands commands_lead_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.commands
    ADD CONSTRAINT commands_lead_id_foreign FOREIGN KEY (lead_id) REFERENCES public.leads(id) ON DELETE SET NULL;


--
-- Name: commands commands_parent_command_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.commands
    ADD CONSTRAINT commands_parent_command_id_foreign FOREIGN KEY (parent_command_id) REFERENCES public.commands(id) ON DELETE SET NULL;


--
-- Name: dm_post_lead dm_post_lead_dm_post_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dm_post_lead
    ADD CONSTRAINT dm_post_lead_dm_post_id_foreign FOREIGN KEY (dm_post_id) REFERENCES public.dm_posts(id) ON DELETE CASCADE;


--
-- Name: dm_post_lead dm_post_lead_lead_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dm_post_lead
    ADD CONSTRAINT dm_post_lead_lead_id_foreign FOREIGN KEY (lead_id) REFERENCES public.leads(id) ON DELETE CASCADE;


--
-- Name: dm_posts dm_posts_category_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dm_posts
    ADD CONSTRAINT dm_posts_category_id_foreign FOREIGN KEY (category_id) REFERENCES public.categories(id) ON DELETE SET NULL;


--
-- Name: hashtags hashtags_category_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hashtags
    ADD CONSTRAINT hashtags_category_id_foreign FOREIGN KEY (category_id) REFERENCES public.categories(id) ON DELETE SET NULL;


--
-- Name: lead_histories lead_histories_account_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lead_histories
    ADD CONSTRAINT lead_histories_account_id_foreign FOREIGN KEY (account_id) REFERENCES public.accounts(id) ON DELETE CASCADE;


--
-- Name: lead_histories lead_histories_lead_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lead_histories
    ADD CONSTRAINT lead_histories_lead_id_foreign FOREIGN KEY (lead_id) REFERENCES public.leads(id) ON DELETE CASCADE;


--
-- Name: lead_histories lead_histories_user_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lead_histories
    ADD CONSTRAINT lead_histories_user_id_foreign FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: lead_sources lead_sources_category_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lead_sources
    ADD CONSTRAINT lead_sources_category_id_foreign FOREIGN KEY (category_id) REFERENCES public.categories(id) ON DELETE SET NULL;


--
-- Name: leads leads_account_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.leads
    ADD CONSTRAINT leads_account_id_foreign FOREIGN KEY (account_id) REFERENCES public.accounts(id) ON DELETE SET NULL;


--
-- Name: leads leads_category_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.leads
    ADD CONSTRAINT leads_category_id_foreign FOREIGN KEY (category_id) REFERENCES public.categories(id) ON DELETE SET NULL;


--
-- Name: leads leads_user_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.leads
    ADD CONSTRAINT leads_user_id_foreign FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: logs logs_account_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.logs
    ADD CONSTRAINT logs_account_id_foreign FOREIGN KEY (account_id) REFERENCES public.accounts(id) ON DELETE CASCADE;


--
-- Name: looms looms_account_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.looms
    ADD CONSTRAINT looms_account_id_foreign FOREIGN KEY (account_id) REFERENCES public.accounts(id) ON DELETE SET NULL;


--
-- Name: looms looms_lead_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.looms
    ADD CONSTRAINT looms_lead_id_foreign FOREIGN KEY (lead_id) REFERENCES public.leads(id) ON DELETE SET NULL;


--
-- Name: messages messages_thread_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_thread_id_foreign FOREIGN KEY (thread_id) REFERENCES public.threads(id) ON DELETE CASCADE;


--
-- Name: notifs notifs_account_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notifs
    ADD CONSTRAINT notifs_account_id_foreign FOREIGN KEY (account_id) REFERENCES public.accounts(id) ON DELETE CASCADE;


--
-- Name: notifs notifs_lead_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notifs
    ADD CONSTRAINT notifs_lead_id_foreign FOREIGN KEY (lead_id) REFERENCES public.leads(id) ON DELETE CASCADE;


--
-- Name: notifs notifs_message_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notifs
    ADD CONSTRAINT notifs_message_id_foreign FOREIGN KEY (message_id) REFERENCES public.messages(id) ON DELETE CASCADE;


--
-- Name: notifs notifs_thread_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notifs
    ADD CONSTRAINT notifs_thread_id_foreign FOREIGN KEY (thread_id) REFERENCES public.threads(id) ON DELETE CASCADE;


--
-- Name: permission_role permission_role_permission_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.permission_role
    ADD CONSTRAINT permission_role_permission_id_foreign FOREIGN KEY (permission_id) REFERENCES public.permissions(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: permission_role permission_role_role_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.permission_role
    ADD CONSTRAINT permission_role_role_id_foreign FOREIGN KEY (role_id) REFERENCES public.roles(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: permission_user permission_user_permission_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.permission_user
    ADD CONSTRAINT permission_user_permission_id_foreign FOREIGN KEY (permission_id) REFERENCES public.permissions(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: profiles profiles_proxy_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.profiles
    ADD CONSTRAINT profiles_proxy_id_foreign FOREIGN KEY (proxy_id) REFERENCES public.proxies(id) ON DELETE SET NULL;


--
-- Name: role_user role_user_role_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.role_user
    ADD CONSTRAINT role_user_role_id_foreign FOREIGN KEY (role_id) REFERENCES public.roles(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: screen_shots screen_shots_account_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.screen_shots
    ADD CONSTRAINT screen_shots_account_id_foreign FOREIGN KEY (account_id) REFERENCES public.accounts(id) ON DELETE CASCADE;


--
-- Name: spintaxes spintaxes_category_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.spintaxes
    ADD CONSTRAINT spintaxes_category_id_foreign FOREIGN KEY (category_id) REFERENCES public.categories(id) ON DELETE SET NULL;


--
-- Name: taggables taggables_tag_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.taggables
    ADD CONSTRAINT taggables_tag_id_foreign FOREIGN KEY (tag_id) REFERENCES public.tags(id) ON DELETE CASCADE;


--
-- Name: templates templates_category_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.templates
    ADD CONSTRAINT templates_category_id_foreign FOREIGN KEY (category_id) REFERENCES public.categories(id) ON DELETE SET NULL;


--
-- Name: templates templates_color_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.templates
    ADD CONSTRAINT templates_color_id_foreign FOREIGN KEY (color_id) REFERENCES public.colors(id) ON DELETE SET NULL;


--
-- Name: threads threads_account_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.threads
    ADD CONSTRAINT threads_account_id_foreign FOREIGN KEY (account_id) REFERENCES public.accounts(id) ON DELETE CASCADE;


--
-- Name: threads threads_category_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.threads
    ADD CONSTRAINT threads_category_id_foreign FOREIGN KEY (category_id) REFERENCES public.categories(id) ON DELETE SET NULL;


--
-- Name: threads threads_lead_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.threads
    ADD CONSTRAINT threads_lead_id_foreign FOREIGN KEY (lead_id) REFERENCES public.leads(id) ON DELETE SET NULL;


--
-- Name: warnings warnings_account_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.warnings
    ADD CONSTRAINT warnings_account_id_foreign FOREIGN KEY (account_id) REFERENCES public.accounts(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

