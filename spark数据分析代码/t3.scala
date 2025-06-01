package DataAnalysis_yds

import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._

import java.util.Properties

object t3 {
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
//      .where(col("sex")===1)
      .createTempView("data")

// todo 分析每种小说的平均字数(万为单位)
    val result = spark.sql(
      """
        |select distinct
        |book_class,
        |round(avg(number_words) over(partition by book_class),2) as avg_number
        |from data
        |""".stripMargin)

    result.write.format("overwrite")
      .jdbc("jdbc:mysql://192.168.40.110:3306/yds?useSSL=false","r3",conn)


    spark.close()
  }

}
