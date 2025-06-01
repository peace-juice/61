package DataAnalysis_yds
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._

import java.util.Properties
object t4 {
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

    //  todo 分析目前字数最多的前10位用户的字数
    val result = spark.sql(
      """
        |select
        |user_name,
        |number
        |from(
        |select distinct
        |user_name,
        |sum(number_words) over(partition by user_name ) as number
        |from data
        |) as r1
        |order by number desc
        |limit 10
        |""".stripMargin)

    result.write.format("overwrite")
      .jdbc("jdbc:mysql://192.168.40.110:3306/yds?useSSL=false","r4",conn)


    spark.close()
  }

}
