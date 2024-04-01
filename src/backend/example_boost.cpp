#include <boost/python.hpp>
#include <iostream>

char easy(){
   return "hello, world";
}

int func(int a, int b){
  return a*b;
}

BOOST_PYTHON_MODULE()
{
    using namespace boost::python;
    def("easy", easy);
    def("func",func);
}
