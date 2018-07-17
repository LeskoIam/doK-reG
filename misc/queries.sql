-- Get complete document history
SELECT
  t2.document_title,
  t2.revision AS revision,
  u.username AS document_owner,
  t2.username AS last_updated_by,
  t2.original_file_name,
  t2.last_updated,
  t2.created,
  t2.comment,
  t2.project_name,
  2 AS document_id
FROM
  (SELECT
    t1.user_id,
    u.username,
    t1.owner_id,
    t1.document_title,
    t1.revision,
    t1.original_file_name,
    t1.last_updated,
    t1.created,
    t1.comment,
    t1.project_name
  FROM
    (SELECT
      r.revision,
      d.owner_id,
      d.title AS document_title,
      r.user_id,
      r.original_file_name,
      r.created_on AS last_updated,
      d.created_on AS created,
      r.comment AS comment,
      p.name AS project_name
    FROM
      document d
    JOIN revision r ON r.document_id = d.id
    JOIN project p ON d.project_id = p.id
    WHERE
      d.active = true AND
      p.active = true AND
      d.id = 2) t1 -- Here is it - document id
  JOIN "user" u ON t1.user_id = u.id) t2
JOIN "user" u ON t2.owner_id = u.id
ORDER BY revision DESC;