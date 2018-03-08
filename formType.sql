-- Table: public."formType"

-- DROP TABLE public."formType";

CREATE TABLE public.formType
(
  id integer NOT NULL,
  noc text,
  amount numeric,
  CONSTRAINT "formType_pkey" PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.formType
  OWNER TO postgres;
