BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "rolls" (
	"order_no"	TEXT,
	"position"	INTEGER,
	"lenght"	INTEGER,
	"weight"	REAL,
	"is_waste"	INTEGER,
	"add_control"	INTEGER,
	"extr_time"	TEXT,
	"extr_author_id"	INTEGER,
	"extr_comment"	TEXT,
	"flex_time"	TEXT,
	"flex_author_id"	INTEGER,
	"flex_comment"	TEXT,
	"cut_time"	TEXT,
	"cut_author_id"	INTEGER,
	"cut_comment"	TEXT,
	"chief_comment"	TEXT
);
COMMIT;
