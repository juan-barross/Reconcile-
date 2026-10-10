# Metabase OSS com o driver DuckDB da MotherDuck (ver ADR 0003).
# A imagem oficial do Metabase é Alpine (musl) e o DuckDB precisa de glibc,
# por isso partimos de uma JRE em Ubuntu.
FROM eclipse-temurin:21-jre-jammy

ARG METABASE_VERSION=v0.63.19
ARG DUCKDB_DRIVER_VERSION=1.5.5.0

ENV MB_PLUGINS_DIR=/home/metabase/plugins
WORKDIR /home/metabase

RUN mkdir -p ${MB_PLUGINS_DIR} \
 && curl -fsSL -o metabase.jar \
      https://downloads.metabase.com/${METABASE_VERSION}/metabase.jar \
 && curl -fsSL -o ${MB_PLUGINS_DIR}/duckdb.metabase-driver.jar \
      https://github.com/motherduckdb/metabase_duckdb_driver/releases/download/${DUCKDB_DRIVER_VERSION}/duckdb.metabase-driver.jar

EXPOSE 3000
CMD ["java", "-jar", "metabase.jar"]
