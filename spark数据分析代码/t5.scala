package DataAnalysis_yds

import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import java.util.Properties

object t5 {
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
      .filter(col("sex")===1)
      .toDF()
      .createTempView("data")

    //  todo 分析男生每种小说类型的数量
    val result = spark.sql(
      """
        |select distinct
        |book_class,
        |count(*) over(partition by book_class) as number
        |from data
        |""".stripMargin)

    result.write.format("overwrite")
      .jdbc("jdbc:mysql://192.168.40.110:3306/yds?useSSL=false","r5",conn)

    spark.close()
  }

}
