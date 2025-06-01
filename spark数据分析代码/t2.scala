package DataAnalysis_yds

import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._

import java.util.Properties


object t2 {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder()
      .master("local[*]")
      .appName("t1")
      .enableHiveSupport()
      .getOrCreate()

    //  todo 配置连接mysql的参数
    val conn = new Properties()
    conn.setProperty("user", "root")
    conn.setProperty("password", "123456")
    conn.setProperty("driver", "com.mysql.jdbc.Driver")

    spark.read
      .jdbc("jdbc:mysql://192.168.40.110:3306/yds?useSSL=false", "dwd", conn)
      .createTempView("data")

    //  todo 分析已经完结和未完结的小说的数量占比
    //  1为未完结，0为完结
    val result = spark.sql(
      """
        |select distinct
        |book_status,
        |count(*) over(partition by book_status) as number
        |from data
        |""".stripMargin)
      .withColumn(
        "book_status",
        when(col("book_status")===1,lit("未完结")).otherwise(lit("完结"))
      )

    result.write.format("overwrite")
      .jdbc("jdbc:mysql://192.168.40.110:3306/yds?useSSL=false","r2",conn)


    spark.close()
  }

}
